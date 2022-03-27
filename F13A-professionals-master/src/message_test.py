'''
test for message
'''
# pylint: disable=unused-variable
# pylint: disable=invalid-name
# pylint: disable=line-too-long
import pytest
from auth import auth_register
from channels import channels_create
from channel import channel_join
from message import message_send, message_react, message_unreact, message_pin, message_unpin, message_remove, message_edit
from data import getData, decode_token
from admin import workspace_reset
from error import InputError, AccessError
#assume that the first people who register an account of Slackr is the owner of Slackr.
## assume that once user create a channel,
## user is immediately added to the channel he create.
def test_message_send_1():
    '''testing message_send running correctly'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password123', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    assert message_send(token, channel_id, 'Hello World!')['message_id'] == 0
def test_message_send_2():
    '''testing the normal user(not admin or owner)in the channel sending a message'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')['token']
    channel_id = channels_create(token_3, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    assert message_send(token_2, channel_id, 'Hello World!')['message_id'] == 0
def test_message_send_input_error_1():
    '''input error because of invalid message input(>1000 characters)'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    with pytest.raises(InputError) as e:
        message_send(token, channel_id, 'ah' * 1001)
def test_message_send_access_error_1():
    '''access error because the authorised user has not joined the channel'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    channel_id = channels_create(token_1, 'Website', True)['channel_id']
    with pytest.raises(AccessError) as e:
        message_send(token_2, channel_id, 'Hello World!')
def test_message_remove_1():
    '''testing message removed by the creator of that message'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    assert message_remove(token, message_id) == {}

def test_message_remove_2():
    '''testing message removed by the owner of channel'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')['token']
    channel_id = channels_create(token_3, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_2, channel_id, 'Hello World!')['message_id']
    assert message_remove(token_3, message_id) == {}

def test_message_remove_3():
    '''testing message removed by the owner of slackr'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')['token']
    channel_id = channels_create(token_3, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_2, channel_id, 'Hello World!')['message_id']
    assert message_remove(token_1, message_id) == {}

def test_message_remove_noMessage():
    '''input error because the message about to be deleted does not exist'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    message_remove(token, message_id)
    with pytest.raises(InputError) as e:
        message_remove(token, message_id)

def test_message_remove_access_error_1():
    '''access error because the authorised user has no privilege'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    channel_id = channels_create(token_1, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_1, channel_id, 'Hello World!')['message_id']
    with pytest.raises(AccessError) as e:
        message_remove(token_2, message_id)
def test_message_edit_1():
    '''testing message edited by the creator of that message'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    assert message_edit(token, message_id, 'World Hello!') == {}
def test_message_edit_2():
    '''testing message edited by the owner of channel'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')['token']
    channel_id = channels_create(token_3, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_2, channel_id, 'Hello World!')['message_id']
    assert message_edit(token_3, message_id, 'World Hello!') == {}
def test_message_edit_3():
    '''testing message edited by the owner of slackr'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password', 'Hayden', 'Smith')['token']
    channel_id = channels_create(token_3, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_2, channel_id, 'Hello World!')['message_id']
    assert message_edit(token_1, message_id, 'World Hello!') == {}
def test_message_edit_emptyMessage():
    '''testing message_edit works when the message is edited as nothing'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    assert message_edit(token, message_id, '') == {}
def test_message_edit_unchangedMessage():
    '''testing message_edit works when the message is not changed'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    assert message_edit(token, message_id, 'Hello World!') == {}
def test_message_edit_longMessage():
    '''input error because of invalid message input(>1000 characters)'''
    workspace_reset()
    token = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    channel_id = channels_create(token, 'Website', True)['channel_id']
    message_id = message_send(token, channel_id, 'Hello World!')['message_id']
    with pytest.raises(InputError) as e:
        message_edit(token, message_id, 'ah' * 1001)
def test_message_edit_access_error_1():
    '''access error because the authorised user has no privilege'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password', 'Jinyu', 'Young')['token']
    channel_id = channels_create(token_1, 'Website', True)['channel_id']
    channel_join(token_2, channel_id)
    message_id = message_send(token_1, channel_id, 'Hello World!')['message_id']
    with pytest.raises(AccessError) as e:
        message_edit(token_2, message_id, 'World Hello!')

def test_message_react_unreact():
    '''Tests for message_react and message_unreact'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password123', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password123', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password123', 'Hayden', 'Smith')['token']
    channel_1 = channels_create(token_3, 'Website', True)
    channel_id_1 = channel_1['channel_id']
    channel_2 = channels_create(token_2, 'Standup', True)
    channel_id_2 = channel_2['channel_id']
    channel_join(token_2, channel_id_1)
    message_1 = message_send(token_2, channel_id_1, 'Hello World!')
    message_id_1 = message_1['message_id']
    message_react(token_2, message_id_1, 1)
    data = getData()
    react_uid_list = data['messages'][message_id_1]['reacts'][0]['u_ids']
    assert decode_token(token_2) in react_uid_list
    with pytest.raises(InputError) as e:
        message_react(token_2, message_id_1, 1)
    invalid_react_id = 2
    with pytest.raises(InputError) as e:
        message_react(token_2, message_id_1, invalid_react_id)
    invalid_message_id = 99
    with pytest.raises(InputError) as e:
        message_react(token_2, invalid_message_id, 1)
    message_2 = message_send(token_2, channel_id_2, 'Hello World!')
    message_id_2 = message_2['message_id']
    with pytest.raises(InputError) as e:
        message_react(token_3, message_id_2, 1)
    message_unreact(token_2, message_id_1, 1)
    data = getData()
    react_uid_list = data['messages'][message_id_1]['reacts'][0]['u_ids']
    assert decode_token(token_2) not in react_uid_list
    with pytest.raises(InputError) as e:
        message_unreact(token_2, message_id_1, 1)
    with pytest.raises(InputError) as e:
        message_unreact(token_2, message_id_1, invalid_react_id)
    with pytest.raises(InputError) as e:
        message_unreact(token_2, invalid_message_id, 1)
    message_react(token_2, message_id_2, 1)
    with pytest.raises(InputError) as e:
        message_unreact(token_3, message_id_2, 1)
def test_message_pin_unpin():
    '''Tests for message_pin and message_unpin'''
    workspace_reset()
    token_1 = auth_register('z5283020@unsw.edu.au', 'password123', 'Jim', 'Yang')['token']
    token_2 = auth_register('z5283021@unsw.edu.au', 'password123', 'Jinyu', 'Young')['token']
    token_3 = auth_register('z5283022@unsw.edu.au', 'password123', 'Hayden', 'Smith')['token']
    channel_1 = channels_create(token_3, 'Website', True)
    channel_id_1 = channel_1['channel_id']
    channel_2 = channels_create(token_2, 'Standup', True)
    channel_id_2 = channel_2['channel_id']
    channel_join(token_2, channel_id_1)
    message_1 = message_send(token_2, channel_id_1, 'Hello World!')
    message_id_1 = message_1['message_id']
    invalid_message_id = 99
    with pytest.raises(InputError) as e:
        message_pin(token_2, invalid_message_id)
    with pytest.raises(InputError) as e:
        message_pin(token_2, message_id_1)
    message_pin(token_3, message_id_1)
    data = getData()
    assert data['messages'][message_id_1]['is_pinned']
    with pytest.raises(InputError) as e:
        message_pin(token_2, message_id_1)
    message_2 = message_send(token_2, channel_id_2, 'Hello World!')
    message_id_2 = message_2['message_id']
    with pytest.raises(AccessError) as e:
        message_pin(token_3, message_id_2)
    with pytest.raises(InputError) as e:
        message_unpin(token_2, invalid_message_id)
    with pytest.raises(InputError) as e:
        message_unpin(token_2, message_id_1)
    message_unpin(token_3, message_id_1)
    data = getData()
    assert not data['messages'][message_id_1]['is_pinned']
    with pytest.raises(InputError) as e:
        message_unpin(token_2, message_id_1)
    message_pin(token_2, message_id_2)
    with pytest.raises(AccessError) as e:
        message_unpin(token_3, message_id_2)
