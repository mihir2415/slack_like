'''
Test functions for admin.py.
'''
import pytest
from admin import admin_permission_change, workspace_reset, admin_user_remove
from auth import auth_register
from data import getData, get_u_id_list
from channel import channel_join
from channels import channels_create
from error import InputError, AccessError
# pylint: disable=invalid-name
# pylint: disable=unused-variable

def member_exist(channel_id, u_id, o_or_a):
    '''check if the member in the owner_members or all_members'''
    data = getData()
    flag = 0
    for member in data['channels'][channel_id][o_or_a]:
        if member['u_id'] == u_id:
            flag = 1
            break
    return flag == 1


def test_workspace_reset():
    '''
    Resets the values in the master data structure to allow for testing on a
    consistent blank initial state.
    '''
    data = getData()
    data['users'] = ['workspace', 'reset']
    assert data['users'] == ['workspace', 'reset']
    workspace_reset()
    assert data['users'] == []

def test_admin_permission_change():
    '''
    Tests if the admin permission value for a user changes correctly. Registers 3 new users
    and then modifies one of thei permission values and then checks for a ID validity and
    then access level with their new permission status.
    '''
    workspace_reset()
    user_info_1 = auth_register('z5283020@unsw.edu.au', 'password123', 'Jim', 'Yang')
    user_info_2 = auth_register('z5283021@unsw.edu.au', 'password123', 'Jinyu', 'Yang')
    user_info_3 = auth_register('z5283022@unsw.edu.au', 'password123', 'hayden', 'smith')
    uid_1 = user_info_1['u_id']
    uid_2 = user_info_2['u_id']
    uid_3 = user_info_3['u_id']
    token_1 = user_info_1['token']
    token_3 = user_info_3['token']
    data = getData()
    assert data['users'][uid_1]['permission_id'] == 1
    assert data['users'][uid_2]['permission_id'] == 2
    assert data['users'][uid_3]['permission_id'] == 2

    admin_permission_change(token_1, uid_2, 1)
    assert data['users'][uid_2]['permission_id'] == 1

    invalid_uid = 404
    with pytest.raises(InputError) as e:
        admin_permission_change(token_1, invalid_uid, 1)

    invalid_permission_id = 3
    with pytest.raises(InputError) as e:
        admin_permission_change(token_1, uid_3, invalid_permission_id)

    #test that the member can't call this function
    with pytest.raises(AccessError):
        admin_permission_change(token_3, uid_2, 2)

def test_admin_user_remove():
    '''
    Tests if the admin permission value for a user changes correctly. Registers 3 new users
    and then modifies oine of thei permission values and then checks for a ID validity and
    then access level with their new permission status.
    '''
    workspace_reset()
    user_info_1 = auth_register('z5283020@unsw.edu.au', 'password123', 'Jim', 'Yang')
    user_info_2 = auth_register('z5283021@unsw.edu.au', 'password123', 'Jinyu', 'Yang')
    user_info_3 = auth_register('z5283022@unsw.edu.au', 'password123', 'hayden', 'smith')
    uid_1 = user_info_1['u_id']
    uid_2 = user_info_2['u_id']
    uid_3 = user_info_3['u_id']
    token_1 = user_info_1['token']
    token_2 = user_info_2['token']
    token_3 = user_info_3['token']
    channel_id = channels_create(token_2, 'Website', True)['channel_id']
    channel_join(token_3, channel_id)
    channel_join(token_1, channel_id)
    data = getData()
    assert member_exist(channel_id, uid_2, 'owner_members') is True
    assert member_exist(channel_id, uid_2, 'all_members') is True
    #test that member can't remove a user
    with pytest.raises(AccessError):
        admin_user_remove(token_2, uid_3)

    #test an invalid user_id
    invalid_uid = 404
    with pytest.raises(InputError):
        admin_user_remove(token_1, invalid_uid)
    #test that the owner remove a user
    admin_user_remove(token_1, uid_2)
    assert uid_1 in get_u_id_list()
    assert uid_2 not in get_u_id_list()
    assert uid_3 in get_u_id_list()
    data = getData()
    assert member_exist(channel_id, uid_2, 'owner_members') is False
    assert member_exist(channel_id, uid_2, 'all_members') is False
