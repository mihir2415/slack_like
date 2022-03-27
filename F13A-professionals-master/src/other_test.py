import pytest
import user
import channel
import channels
import message
import auth

def test_users_all():

    # Creating users to test the function

    user_1 = auth.auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
    all_users = other.users_all(user_1['token'])
    user_profile_1 = user.user_profile(user_1['token'], user_1['u_id'])

    # Assuming the data is stored in the order of the input

    assert user_profile_1['user']['u_id'] == all_users['users'][0]['u_id']
    assert user_profile_1['user']['email'] == all_users['users'][0]['email']
    assert user_profile_1['user']['name_first'] == all_users['users'][0]['name_first']
    assert user_profile_1['user']['name_last'] == all_users['users'][0]['name_last']
    assert user_profile_1['user']['handle_str'] == all_users['users'][0]['handle_str']

    assert len(all_users['users']) == 1


def test_search():

    user_1 = auth.auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
    user_2 = auth.auth_register("hayden@usyd.com", "securitystring2", "Hayden", "Jordan")
    # checks that there is no output for messages when there are no channels
    #no_message = other.search(user_1['token'], 'Sample')
    #assert len(no_message['messages']) == 0

    # Creating 4 channels
    # Channels 1 & 3 are owned by user_1

    new_channel_1 = channels.channels_create(user_1['token'], 'channel_1', True)
    new_channel_2 = channels.channels_create(user_2['token'], 'channel_2', True)
    channel.channel_addowner(user_1['token'], new_channel_1, user_1['u_id'])
    channel.channel_addowner(user_1['token'], new_channel_2, user_2['u_id'])
    channel.channel_join(user_2['token'], new_channel_1)
    channel.channel_join(user_1['token'], new_channel_2)

    # Channels 2 & 4 are owned by user_2
    new_channel_3 = channels.channels_create(user_1['token'], 'channel_3', True)
    new_channel_4 = channels.channels_create(user_2['token'], 'channel_4', True)
    channel.channel_addowner(user_1['token'], new_channel_3, user_1['u_id'])
    channel.channel_addowner(user_1['token'], new_channel_4, user_2['u_id'])
    channel.channel_join(user_1['token'], new_channel_4)

    key_search = "Professionals"
    no_key_search = "Loser"

    msg_1 = message.message_send(user_2['token'], new_channel_1, key_search)
    msg_2 = message.message_send(user_2['token'], new_channel_2, no_key_search)
    msg_3 = message.message_send(user_2['token'], new_channel_3, key_search)
    message.message_send(user_2['token'], new_channel_4, no_key_search)

    # As user_2 is not a part of channel_3, the key_search will not return the key

    result = other.search(user_2['token'], key_search)
    assert len(result['messages']) == 1
    for message in result['messages']:
        assert message['u_id'] == user_1['u_id']
