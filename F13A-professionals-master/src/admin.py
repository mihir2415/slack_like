'''
admin function and workspace function
'''

from error import AccessError, InputError
from data import getData, decode_token, uid_data

def find_member(u_id):
    '''get an u_id and return a member'''
    data = getData()
    for user in data['users']:
        if u_id == user['u_id']:
            return {
                'u_id': u_id,
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }
    return {}

def admin_permission_change(token, u_id, permission_id):
    '''owner of Slackr use these function to change member's permission'''
    data = getData()
    my_u_id = decode_token(token)
    if data['users'][my_u_id]['permission_id'] == 2:
        raise AccessError(description='the authorised user is not an owner')
    tar_user = uid_data(u_id)
    if permission_id not in (1, 2):
        raise InputError(description='permission_id is invalid')
    tar_user['permission_id'] = permission_id
    return {}

def admin_user_remove(token, u_id):
    '''remove the user by owner of Slackr'''
    data = getData()
    my_u_id = decode_token(token)
    if data['users'][my_u_id]['permission_id'] == 2:
        raise AccessError(description='the authorised user is not an owner')
    #remove the user in user file
    flag = 0
    for user in data['users']:
        if user['u_id'] == u_id:
            flag = 1
            member = find_member(u_id)
            user_channel = user['user_channel']
            data['users'].remove(user)
    if flag == 0:
        raise InputError(description='u_id is invalid')
    #remove user from all the channel he join
    if user_channel:
        for channel in user_channel:
            data['channels'][channel['channel_id']]['all_members'].remove(member)
            if member in data['channels'][channel['channel_id']]['owner_members']:
                data['channels'][channel['channel_id']]['owner_members'].remove(member)

def workspace_reset():
    '''reset the data structure'''
    data = getData()
    data['users'] = []
    data['channels'] = []
    data['messages'] = []
    return {}
