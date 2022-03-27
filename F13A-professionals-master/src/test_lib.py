import pytest
from auth import auth_login, auth_logout, auth_register
from error import InputError
from admin import workspace_reset
from channels import channels_create, channels_list, channels_listall
from channel import channel_addowner, channel_details, channel_invite, channel_join, channel_leave, channel_removeowner
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname, users_all

def test_logout_login():
    workspace_reset()
    token = auth_register("z5254608@unsw.edu.au", "professionals", "Brent", "Tonisson")
    assert token['u_id'] == 0
    assert auth_logout(token['token']) == {'is_success': True}
    token1 = auth_login("z5254608@unsw.edu.au", "professionals")
    assert token1['u_id'] == 0
    channel_id1 = channels_create(token1['token'], "professionals", True)
    assert channel_id1 == 0
    token2 = auth_register('z5283021@unsw.edu.au', 'password123', 'Jinyu', 'Yang')
    assert token2['u_id'] == 1
    channel_id2 = channels_create(token2['token'], 'F13A', False)
    assert channel_id2 == 1
    assert channels_listall(token2['token']) == [{'channel_id' : 0, 'name' : 'professionals'}, {'channel_id' : 1, 'name' : 'F13A'}]
    assert channels_list(token2['token']) == [{'channel_id' : 1, 'name' : 'F13A'}]
    assert channel_invite(token1['token'], 0, 1) == {}
    assert channel_details(token1['token'], 0) == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    channel_leave(token2['token'], 0)
    assert channel_details(token1['token'], 0) == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}]}
    channel_join(token2['token'], 0)
    assert channel_details(token1['token'], 0) == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    channel_addowner(token1['token'], 0, 1) 
    assert channel_details(token1['token'], 0) == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    channel_removeowner(token1['token'], 0, 1) 
    assert channel_details(token1['token'], 0) == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    assert user_profile(token1['token'], 0) == {'user': {'email': 'z5254608@unsw.edu.au', 'handle_str': 'BrentTonisson', 'name_first': 'Brent', 'name_last': 'Tonisson', 'u_id': 0}}
    user_profile_setname(token1['token'], 'Hayden', 'Smith')
    user_profile_setemail(token1['token'], 'z5283022@unsw.edu.au')
    user_profile_sethandle(token1['token'], 'haydensmith')
    assert user_profile(token1['token'], 0) == {'user': {'email': 'z5283022@unsw.edu.au', 'handle_str': 'haydensmith', 'name_first': 'Hayden', 'name_last': 'Smith', 'u_id': 0}}
    assert users_all(token1['token']) == {'users': [{'user': {'email': 'z5283022@unsw.edu.au', 'handle_str': 'haydensmith', 'name_first': 'Hayden', 'name_last': 'Smith', 'u_id': 0}}, {'user': {'email': 'z5283021@unsw.edu.au', 'handle_str': 'JinyuYang', 'name_first': 'Jinyu', 'name_last': 'Yang', 'u_id': 1}}]}
