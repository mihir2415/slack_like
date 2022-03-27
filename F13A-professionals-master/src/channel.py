'''
- Ability to create a channel, join a channel, invite someone
else to a channel, and leave a channel
- Within a channel, ability to view all messages, view the members
of the channel, and the details of the channel
- Within a channel, ability to send a message now, or
to send a message at a specified time in the future
- Within a channel, ability to edit, remove, pin,
unpin, react, or unreact to a message
'''
from data import getData, check_channel_id, find_channel, decode_token, uid_data
from error import AccessError, InputError

def channel_messages(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised
    user is part of, this func. returns up to 50 messages between index
    "start" and "start + 50" exclusive. Message with index 0
    is the most recent message in the channel.
    This function returns a new index "end" which is
    the value of "start + 50", or, if this function
    has returned the least recent messages in the channel,
    returns -1 in "end" to indicate there are no more
    messages to load after this return.
    '''
    data = getData()
    #This function checks if the token is valid and retrieves the u_id '''
    u_id = decode_token(token)
    #The function called chacks if the channel_id is valid '''
    channel_id = check_channel_id(int(channel_id))

    #The use of flags result in checking if the user is the part of the channel or not '''
    channel = {}
    for chan in data['channels']:
        if chan['channel_id'] == channel_id:
            channel = chan
            for user in chan['all_members']:
                if user['u_id'] == u_id:
                    break
            else:
                raise AccessError(description='You are not a part of the specified channel...')

    #Checks whether the start value is greater than the number of messages '''
    message_stored = channel['messages']
    start = int(start)
    if start > len(message_stored):
        raise InputError(description='The start value entered is more than the existing messages')
    message_stored.reverse()

    end = start + 50

    if end >= len(channel['messages']):
        end = len(channel['messages'])

    #Data to return
    to_return = {
        'messages':message_stored[start:end],
        'start':start,
        'end' : end
    }

    #end has to be -1 if we are at the end of messages
    if end == len(channel['messages']):
        to_return['end'] = -1

    return to_return

def channel_details(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised
    user is part of, provides basic details about the channel
    '''
    data = getData()
    #This function checks if the token is valid and retrieves the u_id '''
    u_id = decode_token(token)
    #The function called chacks if the channel_id is valid '''
    channel_id = check_channel_id(int(channel_id))
    #The use of flags result in checking if the user is the part of the channel or not '''
    for i_de in data['channels']:
        if i_de['channel_id'] == channel_id:
            channel = i_de
            break

    for user in channel['all_members']:
        if user['u_id'] == u_id:
            break
    else:
        raise AccessError('You are not a part of the specified channel...')
    #The below mentioned code checks if the channel_id matches the one passed '''
    for chan in data['channels']:
        if chan['channel_id'] == channel_id:
            return {
                'name':chan['channel_name'],
                'owner_members':chan['owner_members'],
                'all_members':chan['all_members']
            }

def channel_join(token, channel_id):
    ''' Given a channel_id and then join to that channel '''
    channel_id = int(channel_id)
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    if find_channel(channel_id) is None:
        raise InputError(description="channel_id  is invalid")
    channel = data['channels'][channel_id]
    if not channel['public']:
        raise AccessError(description="This is a private channel that cant join")
    user_is_joined = False
    for each_user_channel in user['user_channel']:
        if channel['channel_id'] == each_user_channel['channel_id']:
            user_is_joined = True
    if not user_is_joined:
        user['user_channel'].append({'channel_id': channel['channel_id'],
                                     'channel_name': channel['channel_name']})
        channel['all_members'].append({'u_id' : user_id, 'name_first' : user['name_first'],
                                       'name_last' : user['name_last']})
    return {}

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user to join a channel with channel_id.
    Once invited the user is added to channel
    '''
    channel_id = int(channel_id)
    data = getData()
    user_id = decode_token(token)
    invite_user = uid_data(u_id)
    if find_channel(channel_id) is None:
        raise InputError(description="channel_id  is invalid")
    is_joined = False
    for user_in_channel in data['users'][user_id]['user_channel']:
        if channel_id == user_in_channel['channel_id']:
            is_joined = True

    if not is_joined:
        raise AccessError(description="the authorised user is not already a member of the channel.")
    channel = data['channels'][channel_id]
    for each_user_channel in invite_user['user_channel']:
        if channel['channel_id'] == each_user_channel['channel_id']:
            break
    else:
        invite_user['user_channel'].append({'channel_id': channel['channel_id'],
                                            'channel_name': channel['channel_name']})
        channel['all_members'].append({'u_id' : u_id, 'name_first' : invite_user['name_first'],
                                       'name_last' : invite_user['name_last']})
    return {}

def channel_leave(token, channel_id):
    ''' Given a channel_id, the user removed from this channel '''
    channel_id = int(channel_id)
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    if find_channel(channel_id) is None:
        raise InputError(description="channel_id  is invalid")
    else:
        channel = data['channels'][channel_id]

    for user_in_channel in data['users'][user_id]['user_channel']:
        if channel_id == user_in_channel['channel_id']:
            break
    else:
        raise AccessError(description="the authorised user is not already a member of the channel.")

    user['user_channel'].remove({'channel_id': channel_id,
                                 'name': channel['channel_name']})
    channel['all_members'].remove({'u_id': user_id, 'name_first': user['name_first'],
                                   'name_last': user['name_last']})
    if user_id in channel['owner_members']:
        channel['owner_members'].remove(user_id)
    return {}

def channel_addowner(token, channel_id, u_id):
    ''' Make user with user id u_id an owner of this channel '''
    channel_id = int(channel_id)
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    new_owner = uid_data(u_id)
    if find_channel(channel_id) is None:
        raise InputError(description="channel_id  is invalid")
    channel = data['channels'][channel_id]
    if u_id in channel['owner_members']:
        raise InputError(description="the user with u_id is already an owner")
    if (user_id not in channel['owner_members']) and (user['permission_id'] != 1):
        raise AccessError(description="The authorised user don't have the right to access")
    channel['owner_members'].append({'u_id' : u_id, 'name_first' : new_owner['name_first'],
                                     'name_last' : new_owner['name_last']})
    return {}

def channel_removeowner(token, channel_id, u_id):
    ''' Remove user with user id u_id an owner of this channel '''
    channel_id = int(channel_id)
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    rem_owner = uid_data(u_id)
    if find_channel(channel_id) is None:
        raise InputError(description="channel_id  is invalid")
    channel = data['channels'][channel_id]
    if user['permission_id'] != 1:
        raise AccessError(description="The authorised user don't have the right to access")
    for user in channel['owner_members']:
        if u_id == user['u_id']:
            break
    else:
        raise AccessError(description="the user with u_id is not an owner")
    channel['owner_members'].remove({'u_id' : u_id, 'name_first' : rem_owner['name_first'],
                                     'name_last' : rem_owner['name_last']})
    return {}
