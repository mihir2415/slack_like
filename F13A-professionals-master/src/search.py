'''
Search function which searches for a query_str and returns the
dictionary for all messages which matches that string.
This funtionality is available only for a user who is
a part of the channel
'''
from data import getData, check_token


def search(token, query_str):
    '''
    Search function which searches for a query_str and returns the
    dictionary for all messages which match that string
    '''
    data = getData()
    #checks if the token is valid and retrieves the uid '''
    u_id = check_token(token)['u_id']
    mess_que = []
    mess_return = []
    for user in data['channels']:
        if user['all_members'] == u_id:
            for mess in user['messages']:
                mess_que.append(mess)
    for m_mess in data['messages']:
        if m_mess in mess_que:
            if query_str in m_mess['message']:
                mess_return.append({
                    'message_id': m_mess['message_id'],
                    'u_id': m_mess['u_id'],
                    'message': m_mess['message'],
                    'time_created': m_mess['time_created'],
                    'reacts': m_mess['reacts'],
                    'is_pinned': m_mess['is_pinned']
                })
    return mess_return
