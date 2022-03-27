'''
Data.py is used across almost all other python files and houses the megastructure we have
implemented for storing users data, as well as channel and message data. The information is
stored in a dictionary 'data', which contains three lists. Each list is a list of dictionaries
containing a specific type of data. Includes functions to manipulate and convenietly access
parts of this data structure.
'''
import re
import pickle
import jwt
import os.path
import time, traceback
from error import AccessError, InputError
'''''''''''''''''''''''
Global variable
'''''''''''''''''''''''
"""
messages:its a list of dictionaries
each dictionary is what one message contains

    {
    'channel_id'
    'message_id',
    'u_id',
    'message',
    'time_created',
    'reacts':[{'react_id':1, 'u_ids'(a list), 'is_this_user_reacted'(boolean)}],
    'is_pinned'
    maybe more..
    }

users:its a list of dictionaries
each dictionary is what one user contains

    {
    'u_id',
    'email',
    'name_first',
    'name_last',
    'handle_str',
    'password' (new added)
    'reset_code'
    'profile_img_url'
    'user_channel':[{'channel_id', 'channel_name'}]
    'permission_id'(new added):'1':owner of slackr
                               '2':member of slackr
                               these are the global permissions
    maybe more..
    }

channels: its a list of dictionaries
each dictionary is what one channel contains
'''
    {
    'channel_id',
    'channel_name',
    'owner_members': ['user_id'],
    'all_members': ['user_id'],
    'messages': ['message_id']
    'public': Boolean
    'standup': { 'is_active': Boolean, 'time_finish':unix_timestamp }
    'standup_mess': ''
    'hangman': { 'is_active': False, 'mistakes': 0, 'word': , 'available':}
    }
"""

# the element in each list is a dictionary
# So my reason for using list is,if you create/remove a new user/channel/message
# you can use append/remove to do that. And the suffix_ID is a good thing as an
# index to locate each info you want in the list (assume the id start from 0, and
# add in order)
data = {
    'users':[],
    'messages':[],
    'channels':[]
}


'''
Helper Functions that everyone can get the data they want.
(You can also add some helper functions to simplify your work)
'''
def uid_data(u_id):
    '''
    given a uid that return all the info from that user
    '''
    flag = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            flag = 1
            return user
    if flag == 0:
        raise InputError(description='u_id is invalid')

def check_token(token):
    '''

    '''
    data = getData()
    if token not in data['token']:
        raise InputError(description='token is invalid')
    else:
        return jwt.decode(token, 'professionals', algorithms='HS256')

def check_channel_id(channel_id):
    '''

    '''
    data = getData()
    for chan_id in data['channels']:
        if chan_id['channel_id'] == channel_id:
            return channel_id
    else:
        raise InputError(description='channel_id is invalid')

def getData():
    '''
    get data from global 'data'
    '''
    global data
    return data

def find_message(message_id):
    '''
    given a message_id and return the index that the message sit in the
    'messages' list. if not return None for no result.
    '''
    data = getData()
    pos = 0
    for message in data['messages']:
        if int(message['message_id']) == message_id:
            return pos
        pos = pos + 1
    return None

# pylint: disable=anomalous-backslash-in-string
def check_email_valid(email):
    '''

    '''
    valid_form = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(valid_form, email):
        return True
    else:
        return False

def get_u_id_list():
    '''
    get all u_ids in whole data structure
    '''
    data = getData()
    u_list = []
    for user in data['users']:
        u_list.append(user['u_id'])
    return u_list

def get_email_list():
    '''
    get all u_ids in whole data structure
    '''
    data = getData()
    email_list = []
    for user in data['users']:
        email_list.append(user['email'])
    return email_list

def get_handle_list():
    '''
    get all u_ids in whole data structure
    '''
    data = getData()
    handle_list = []
    for user in data['users']:
        handle_list.append(user['handle_str'])
    return handle_list

def generate_token(u_id):
    '''

    '''
    token = jwt.encode({'users_id': u_id}, 'professionals', algorithm='HS256').decode('utf-8')
    return str(token)

def decode_token(token):
    '''

    '''
    decoded_token = jwt.decode(token, 'professionals', algorithms=['HS256'])
    return decoded_token['users_id']



def add_new_user(email, password, name_first, name_last, handle, u_id, token):
    '''

    '''
    data = getData()
    if u_id == 0:
        new_user = {
            'u_id' : u_id,
            'email' : email,
            'name_first' : name_first,
            'name_last' : name_last,
            'handle_str' : handle,
            'password' : password,
            'reset_code' : None,
            'profile_img_url': '',
            'user_channel':[],
            'permission_id' : 1
        }
    else:
        new_user = {
            'u_id' : u_id,
            'email' : email,
            'name_first' : name_first,
            'name_last' : name_last,
            'handle_str' : handle,
            'password' : password,
            'reset_code' : None,
            'profile_img_url': '',
            'user_channel':[],
            'permission_id' : 2
        }
    data['users'].append(new_user)


def check_valid_token(token):
    '''

    '''
    temp_id = decode_token(token)
    id_list = get_u_id_list()
    if temp_id in id_list:
        return True
    else:
        raise AccessError(description="authorisation is required")

def invalidate_token(token):
    '''

    '''
    temp_id = decode_token(token)

def new_message_id():
    '''

    '''
    data = getData()
    if len(data['messages']) == 0:
        return 0
    return data['messages'][len(data['messages']) - 1]['message_id'] + 1

def find_channel(channel_id):
    '''

    '''
    data = getData()
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return None

def time_interval(delay):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        
        try:
            persist_data()
        except Exception:
            traceback.print_exc()

        # skip calls of persist_data if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay

def persist_data():
    temp_data = getData()
    f = open('storeddata.pkl', 'wb', -1)
    pickle.dump(temp_data ,f)
    f.close()

def establish_data():
    if os.path.isfile('storeddata.pkl'):
        f = open('storeddata.pkl', 'rb')
        temp_data = pickle.load(f)
        f.close()
        global data
        data = temp_data
        
def update_profile_image(url, u_id):
    '''

    '''
    data = getData()
    for user in data['users']:
        if user['u_id'] == u_id:
            user['profile_img_url'] = url
