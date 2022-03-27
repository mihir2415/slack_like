'''
For a given channel, the standup starts a period whereby
for the next "length" seconds if someone calls "standup_send"
with a message, it is buffered during the X second window
then at the end of the X second window a message will be
added to the message queue in the channel from the user
who started the standup.
'Length' is an integer that denotes the number of seconds
that the standup occurs for
'''

from datetime import datetime
from data import getData, check_token, check_channel_id, decode_token
from error import AccessError

def start_standup(token, channel_id, length):
    '''
    starts the standup by calculating the time_finish
    '''
    data = getData()
    #The function called chacks if the channel_id is valid '''
    channel_id = check_channel_id(channel_id)
    #This function checks if the token is valid and retrieves the u_id '''
    u_id = check_token(token)['u_id']
    #Checking if the channel_id matches the one passed then everything is copied in a new
    #dictionary created called 'channel'
    channel = {}
    for s_chan in data['channels']:
        if s_chan['channel_id'] == channel_id:
            channel = s_chan.copy()
    #Checking if the user is part of the passed channel '''
    flag = 0
    for i in channel['all_members']:
        if i == u_id:
            flag = 1
    if flag == 0:
        raise AccessError('You are not a part of this channel...')
    #If user is a part of the channel then the standup becomes active '''
    channel['standup']['is_active'] = True
    now = datetime.now()
    #Setting the time of the standup '''
    timestamp = datetime.timestamp(now)
    standup_time = timestamp + length
    channel['standup']['time_finish'] = standup_time
    for s_cha in data['channels']:
        if s_cha['channel_id'] == channel_id:
            s_cha['standup'] = channel['standup'].copy()
    return {
        'time_finish': channel['standup']['time_finish']
    }

def active_standup(token, channel_id):
    '''
    checks whether the standup is active and also when it finishes
    '''
    data = getData()
    channel_id = check_channel_id(int(channel_id))
    u_id = decode_token(token)
    for s_chan in data['channels']:
        if s_chan['channel_id'] == channel_id:
            if u_id in s_chan['all_members']:
                return {
                    'is_active': s_chan['standup']['is_active'],
                    'time_finish': s_chan['standup']['time_finish']
                }


def send_standup(token, channel_id, message):
    '''
    Sends all the messages to a specified created buffer
    '''
    data = getData()
    channel_id = check_channel_id(channel_id)
    u_id = check_token(token)['u_id']
    #Adds a new line if there is already a message in the buffer '''
    counter = []
    if len(counter) >= 1:
        new_message = "/n" + data['users']['handle_str'] + ":" + message
    else:
        new_message = data['users']['handle_str'] + ":" + message
    for s_chan in data['channels']:
        if s_chan['channel_id'] == channel_id:
            if u_id in s_chan['all_members']:
                s_chan['standup_mess'] += new_message
                counter.append(1)
            else:
                raise AccessError(description = 'You are not a part of this channel!')
