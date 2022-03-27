'''
Module containing all the channel functions
'''
from data import decode_token, getData, check_valid_token
from error import InputError, AccessError

def generate_channel_id(data):
    '''
    Function that generates a channel ID.
    '''
    channel_id_list = []
    for channel in data['channels']:
        channel_id_list.append(channel['channel_id'])
    new_cid = len(channel_id_list)
    while new_cid in channel_id_list:
        new_cid += 1
    return new_cid

def channels_list(token):
    '''
    Function to return list of channels a user is in.
    '''
    data = getData()
    user_id = decode_token(token)
    for user in data['users']:
        if user_id == user['u_id']:
            return {'channels': user['user_channel']}
    return {'channels': []}

def channels_listall(token):
    '''
    Function to return a list of all channels in the slackr.
    '''
    data = getData()
    channel_list = []
    for channel in data['channels']:
        channel_list.append({
            'channel_id': channel['channel_id'],
            'name': channel['channel_name']})
    return {'channels': channel_list}
    raise AccessError(description="Access not allowed")

def channels_create(token, name, is_public):
    '''
    Function creates a channel, given the token, channel name and public status.
    '''
    # Check if channel name is empty
    if name == "":
        raise InputError(description="Please enter a channel name")
    # Check if channel name exceeds 20 characters
    if len(name) > 20:
        raise InputError(description="Channel name must not exceed 20 characters")
    data = getData()
    # Check if channel name is already in use
    for channel in data['channels']:
        if channel['channel_name'] == name:
            raise InputError("Channel name already in use")
    # Create the channel
    user_id = decode_token(token)
    channel_id = generate_channel_id(data)
    new_channel = {
        'channel_id': channel_id,
        'channel_name': name,
        'owner_members': [],
        'all_members': [],
        'messages': [],
        'standup': {},
        'standup_mess': [],
        'public': is_public,
        'standup': { 'is_active': False, 'time_finish':0 },
        'standup_mess': '',
        'hangman': { 'is_active': False, 'mistakes': 0, 'word': "", 'available': "abcdefghijklmnopqrstuvwxyz", 'guess': []}
    }
    data['channels'].append(new_channel)
    for user in data['users']:
        if user_id == user['u_id']:
            user['user_channel'].append({
                'channel_id': new_channel['channel_id'],
                'name': new_channel['channel_name']})
            new_channel['owner_members'].append({'u_id' : user['u_id'], 'name_first' : user['name_first'], 'name_last' : user['name_last']})
            new_channel['all_members'].append({'u_id' : user['u_id'], 'name_first' : user['name_first'], 'name_last' : user['name_last']})
    return {'channel_id': new_channel['channel_id']}
