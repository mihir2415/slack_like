from auth import auth_register
from admin import workspace_reset
from channels import *
import pytest
from error import InputError, AccessError

"""
Tests for channels_create
"""
# testing channels_create running correctly

## assume that once user create a channel, 
## user is immediately added to the channel he create.
def test_channels_create_1():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    assert channels_create(login['token'], 'Website', True) == 0

def test_channels_create_2():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    assert channels_create(login['token'], 'Invisible', False) == 0
# input errors for channels_create

## input error because of invalid channel_name(>20 characters).
def test_channels_create_longName():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    with pytest.raises(InputError) as e:
        channels_create(login['token'], 'idontknowwhatnametoputtomychannel', True)

## input error because of invalid channel_name(null).
def test_channels_create_noName():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    with pytest.raises(InputError) as e:
        channels_create(login['token'], '', True)

##assume that channels can't be created if the channel_name is existed

def test_channels_create_same_channelsName():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    channels_create(login['token'], 'Professionals', True)
    with pytest.raises(InputError) as e:
        channels_create(login['token'], 'Professionals', True)


"""
Tests for channels_list
"""

## assume 'channels_list' run normally if there is no channel
def test_channels_list_1():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    assert channels_list(login['token']) == []

## 'channels_list' run correctly in normal situation
## assume channels_create works
def test_channels_list_2():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    channel_id_1 = channels_create(login['token'], 'Professionals_1', False)
    channel_id_2 = channels_create(login['token'], 'Professionals_2', True)
    assert channels_list(login['token']) == [{'channel_id': channel_id_1, 'name': 'Professionals_1'}, {'channel_id': channel_id_2, 'name': 'Professionals_2'}]

    
"""
Tests for channels_listall
"""

# testing channels_listall running correctly

## assume 'channels_listall' run normally even there is no channel
## and return an empty list of dictionary.
def test_channels_listall_1():
    workspace_reset()
    login = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    assert channels_listall(login['token']) == []

## 'channels_listall' run correctly in normal situation
## assume the authorised user can only see the channel which is:
## 1.Public OR 2.user has joined in already
## assume channels_create works
def test_channels_listall_2():
    workspace_reset()
    login_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    login_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Yang')
    channel_id_1 = channels_create(login_1['token'], 'Professionals_1', True)
    channel_id_2 = channels_create(login_2['token'], 'Professionals_2', True)
    assert channels_listall(login_1['token']) == [{'channel_id': channel_id_1, 'name': 'Professionals_1'}, {'channel_id': channel_id_2, 'name': 'Professionals_2'}]
    
def test_channels_listall_3():
    workspace_reset()
    login_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')
    login_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Yang')
    login_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')
    channel_id_1 = channels_create(login_1['token'], 'Professionals_1', False)
    channel_id_2 = channels_create(login_2['token'], 'Professionals_2', True)
    assert channels_listall(login_3['token']) == [{'channel_id': channel_id_1, 'name': 'Professionals_1'}, {'channel_id': channel_id_2, 'name': 'Professionals_2'}]

