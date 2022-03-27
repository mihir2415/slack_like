'''
test for channel.py
'''
# pylint: disable=line-too-long
# pylint: disable=unused-variable
import pytest
from channel import channel_messages, channel_details, channel_join, channel_invite, channel_leave, channel_addowner, channel_removeowner
from channels import channels_create
from auth import auth_register
from admin import workspace_reset
from data import decode_token, getData
from error import InputError, AccessError
def test_channel_invite():
    '''
    Result when assuming there is no error. Assumption is made
    no value is returned and the user is immediately added to channel.
    Given that token is a string and IDs are integers.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    # Result when assuming there is no error. Assumption is made
    # no value is returned and the user is immediately added to channel.
    # Given that token is a string and IDs are integers.
    channel_invite(token_1, channel_id, u_id)
    data = getData()
    assert data['channels'][channel_id]['all_members'][1]['u_id'] == u_id

def test_channel_invite_input_error1():
    '''
    Input error because of unauthorised user.
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
    # Assumes the channel is invalid because the
    # user is unauthorised for the channel (it may not exist).
        assert channel_invite(token, 7, 20562)

def test_channel_invite_input_error2():
    '''
    Input error because of wrong data type input.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    channels_create(token_1, 'Website', True)
    u_id_2 = decode_token(token_2)
    with pytest.raises(InputError):
        channel_invite(token_1, "channel_no", u_id_2)

def test_channel_invite_input_error3():
    '''
    Input error because of no channel number.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    with pytest.raises(InputError):
        channel_invite(token_1, "", u_id_2)

def test_channel_invite_input_error5():
    '''
    Assuming the User ID is invalid because its not an integer (float)
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channel_id = channels_create(token, 'Website', True)
    with pytest.raises(InputError):
        channel_invite(token, channel_id, 30.500)

def test_channel_invite_input_error6():
    '''
    Assuming the User ID is invalid because its was null
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channel_id = channels_create(token, 'Website', True)
    with pytest.raises(InputError):
        channel_invite(token, channel_id, "")

def test_channel_invite_access_error():
    '''
    Assumes the User ID is not a member of the channel (is a valid channel)
    Assumes channel_invite can determine this case.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    token_3 = auth_register('z5254610@unsw.edu.au', 'password', 'Brent', 'Tonisso')['token']
    u_id_2 = decode_token(token_2)
    u_id_3 = decode_token(token_3)
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(AccessError):
        channel_invite(token_2, channel_id, u_id_3)

def test_channel_details1():
    '''
    Assuming the channel ID is valid for the user
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channel_id = channels_create(token, 'Website', True)
    #Assuming the channel ID is valid for the user
    assert channel_details(token, channel_id) == {
        'name': 'Website',
        'owner_members': [
            {
                'u_id': 0,
                'name_first': 'Brent',
                'name_last': 'Tonisson',
            }
        ],
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'Brent',
                'name_last': 'Tonisson',
            }
        ],
    }

def test_channel_details2():
    '''
    Additional test that assumes the group has 2 members but only one is
    # an owner.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id)
    assert channel_details(token_1, channel_id) == {
        'name': 'Website',
        'owner_members': [
            {
                'u_id': 0,
                'name_first': 'Brent',
                'name_last': 'Tonisson',
            }
        ],
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'Brent',
                'name_last': 'Tonisson',
            },
            {
                'u_id': 1,
                'name_first': 'Brent',
                'name_last': 'Tonissom',
            }
        ],
    }

def test_channel_details_input_error1():
    '''
    Assumes that the channel is invalid because it doesn't exist.
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channels_create(token, 'Website', True)
    with pytest.raises(InputError):
        channel_details(token, 74)

def test_channel_details_input_error2():
    '''
    invalid channel_id
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channels_create(token, 'Website', True)
    with pytest.raises(InputError):
        channel_details(token, "channel")

def test_channel_details_input_error3():
    '''
    empty channel_id
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    channels_create(token, 'Website', True)
    with pytest.raises(InputError):
        channel_details(token, "")

def test_channel_details_access_error():
    '''
    Assumes that the user is not an authorised user of the channel
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(AccessError):
        channel_details(token_2, channel_id)

def test_get_messages1():
    '''
    Assumes channel_id is valid and value of start is less or equal
    to the total number of messages in the channel.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    channel_id = channels_create(token_1, 'Website', True)

    # Assumes channel_id is valid and value of start is less or equal
    # to the total number of messages in the channel.
    assert channel_messages(token_1, channel_id, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def test_get_messages2():
    '''
    Assumes channel_id is valid and value of start is less or equal
    to the total number of messages in the channel.
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    assert channel_messages("another example", 5678, 15) == {
        'messages': [
            {
                'message_id': 15,
                'u_id': 1,
                'message': '15th message',
                'time_created': 1582424567,
            }
        ],
        'start': 15,
        'end': 65,
    }

def test_get_messages3():
    '''
    Assume there are less than 65 messages in chat
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    assert channel_messages("message example", 5678, 15) == {
        'messages': [
            {
                'message_id': 15,
                'u_id': 1,
                'message': '15th message',
                'time_created': 1582424567,
            }
        ],
        'start': 15,
        'end': -1,
    }

def test_get_messages_input_error1():
    '''
    Assume that Channel ID is invalid because it doesn't exist.
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
        channel_messages(token, 347, 5)

def test_get_messages_input_error2():
    '''
    Incorrect data type for Channel ID
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
        channel_messages(token, "channel", 5)

def test_get_messages_input_error3():
    '''
    Null data type for Channel ID
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
        channel_messages(token, "", 3)

def test_get_messages_input_error4():
    '''
    assume that start is larger than number of messages in channel
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
        channel_messages(token, 2567, 57)

def test_get_messages_access_error():
    '''
    Assumes that user is not authorised in the channel
    '''
    workspace_reset()
    token = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    with pytest.raises(InputError):
        channel_messages(token, 347, 5)

def test_channel_leave():
    '''
    Assume that channel_id is valid and user is is a member of the channel
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_1 = decode_token(token_1)
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    assert channel_leave(token_2, channel_id) == {}
    data = getData()
    assert data['channels'][channel_id]['all_members'][0]['u_id'] == 0

def test_channel_leave_input_error1():
    '''
    Channel ID invalid because of incorrect data type (must be integer)
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_1 = decode_token(token_1)
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_leave(token_1, "channel")
def test_channel_leave_input_error2():
    '''
    Channel ID invalid because Channel Number doesn't exist
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_1 = decode_token(token_1)
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_leave(token_1, 1353)

def test_channel_leave_input_error3():
    '''
    Channel ID invalid because null input
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_1 = decode_token(token_1)
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_leave(token_1, "")

def test_channel_leave_access_error4():
    '''
    Channel ID invalid because user is unathorised in channel.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(AccessError):
        channel_leave(token_2, channel_id)

def test_channel_join():
    '''
    assuming that the channel is valid and is not private.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    # assuming that the channel is valid and is not private.
    channel_join(token_2, channel_id)
    data = getData()
    assert u_id_2 in data['channels'][channel_id]['all_members']

def test_channel_join_input_error1():
    '''
    Channel ID invalid because of incorrect data type (must be integer)
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(InputError):
        channel_join(token_2, "channel")

def test_channel_join_input_error2():
    '''
    Channel ID invalid because Channel Number doesn't exist
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(InputError):
        channel_join(token_2, 1353)

def test_channel_join_input_error3():
    '''
    Channel ID invalid because null input
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    with pytest.raises(InputError):
    # Channel ID invalid because null input
        assert channel_join(token_2, "")

def test_channel_join_access_error():
    '''
    Channel ID invalid because the channel is private
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', False)
    with pytest.raises(AccessError):
    # Channel ID invalid because the channel is private
        assert channel_join(token_2, channel_id)

def test_channel_addowner():
    '''
    Assuming the Channel ID and User ID are both valid
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    assert channel_addowner(token_1, channel_id, u_id_2) == {}
    data = getData()
    assert u_id_2 in data['channels'][channel_id]['owner_members']
def test_channel_addowner_input_error1():
    '''
    Assuming the Channel ID doesn't exist
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_addowner(token_1, 2472, u_id_2)
def test_channel_addowner_input_error3():
    '''
    Channel ID invalid because of incorrect data type (must be integer)
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_addowner(token_1, "channel", u_id_2)
def test_channel_addowner_input_error5():
    '''
    Channel ID invalid because of null input
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_addowner(token_1, "", u_id_2)
def test_channel_addowner_access_error():
    '''
    Assuming the user isn't an owner of the Slackr or channel.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    channel_id = channels_create(token_1, 'website', True)
    u_id = decode_token(token_1)
    with pytest.raises(AccessError):
    # Assuming the user isn't an owner of the Slackr or channel.
        assert channel_addowner(token_2, u_id, 0)

def test_channel_removeowner():
    '''
    Assuming the Channel ID and User ID are both valid
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    channel_addowner(token_1, channel_id, u_id_2)
    assert channel_removeowner(token_1, channel_id, u_id_2) == {}
def test_channel_removeowner_input_error1():
    '''
    Assuming the Channel ID doesn't exist
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    channel_addowner(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_removeowner(token_1, 141241, u_id_2)
def test_channel_removeowner_input_error3():
    '''
    Channel ID invalid because of incorrect data type (must be integer)
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    channel_addowner(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_removeowner(token_1, "channel", u_id_2)
def test_channel_removeowner_input_error5():
    '''
    Channel ID invalid because of null input
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    u_id_2 = decode_token(token_2)
    channel_id = channels_create(token_1, 'Website', True)
    channel_invite(token_1, channel_id, u_id_2)
    channel_addowner(token_1, channel_id, u_id_2)
    with pytest.raises(InputError):
        channel_removeowner(token_1, "", u_id_2)
def test_channel_removeowner_access_error():
    '''
    Assuming the user isn't an owner of the Slackr or channel.
    '''
    workspace_reset()
    token_1 = auth_register('z5254608@unsw.edu.au', 'password', 'Brent', 'Tonisson')['token']
    token_2 = auth_register('z5254609@unsw.edu.au', 'password', 'Brent', 'Tonissom')['token']
    channel_id = channels_create(token_1, 'website', True)
    u_id = decode_token(token_2)
    channel_join(token_2, channel_id)
    with pytest.raises(AccessError):
    # Assuming the user isn't an owner of the Slackr or channel.
        assert channel_removeowner(token_2, channel_id, u_id)
