from nltk.corpus import brown
from random import randint
from data import *
from datetime import datetime, timezone
from error import AccessError, InputError
'''''
Some message related functions
'''''

def add_standup_message(u_id, channel_id):
    data = getData()
    ''' The function called checks if the channel_id is valid '''
    channel_id = check_channel_id(channel_id)
    ''' Creating a temperory dictionary to check whether the passed channel matches the one stored in data.py '''
    temp_stan = {}
    for stan in data['channels']:
        if stan['channel_id'] == channel_id:
            temp_stan = stan.copy()
    ''' Setting the time_sent as the 'time_finish' as derived in 'standup.py' '''
    time_sent = channel['standup']['time_finish']

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    ''' Setting a condition to add the message in the dictionary only if the time_sent is less or equal to the curr time '''
    if timestamp >= time_sent:
        if len(temp_stan[standup_mess]) > 0:
            '''check if the message is valid in length'''
            if len(message) > 1000:
                raise InputError(description = "Message is over 1000 characters")
        message_id = new_message_id()
        data['messages'].append({'channel_id': channel_id,
                                'message_id': message_id,
                                'u_id': user['u_id'],
                                'message': message,
                                'time_created': time_sent,
                                'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': None}],
                                'is_pinned': False})


def message_send(token, channel_id, message):
    ''' Send a message from authorised_user to channel'''
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    message_id = new_message_id()
    channel_id = check_channel_id(int(channel_id))
    channel = data['channels'][channel_id]   
    '''Error'''

    '''
    This adds a message to the data.py if there are any left in the buffer 
    add_standup_message(user_id, channel_id)
    '''
    '''check if the message is valid in length'''
    if len(message) > 1000:
        raise InputError(description ="Message is over 1000 characters")

    '''check if the the authorised user has joined the channel'''
    is_joined = False
    for user_in_channel in data['users'][user_id]['user_channel']:
        if channel_id == user_in_channel['channel_id']:
            is_joined = True

    if is_joined == False:
        raise AccessError("authorised user has not joined the channel that he wants to post to")

    '''Implementation'''

    data['messages'].append({'channel_id': channel_id,
                            'message_id': message_id,
                            'u_id': user['u_id'],
                            'message': message,
                            'time_created': datetime.timestamp(datetime.now()),
                            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': None}],
                            'is_pinned': False})
    channel['messages'].append({'channel_id': channel_id, 'message_id': message_id,
                            'u_id': user['u_id'],
                            'message': message,
                            'time_created': datetime.timestamp(datetime.now()),
                            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': None}],
                            'is_pinned': False})
                            
    if message == "/hangman":
        run_hangman(token, channel_id, data)
    elif message[:6] == "/guess":
        get_guess(message, token, channel_id, data)
    return {'message_id': message_id}

def message_sendlater(token, channel_id, message, time_sent):
    ''' Send a message from authorised_user to channel in a set time'''
    data = getData()
    user_id = decode_token(token)
    user = data['users'][user_id]
    message_id = new_message_id()

    '''Error'''

    '''check if the channel_id is valid'''
    if find_channel(channel_id) == None:
       raise InputError(description ="channel_id that want to post is invalid")

    '''check if the message is valid in length'''
    if len(message) > 1000:
        raise InputError(description ="Message is over 1000 characters")

    '''check if time sent is a time in the past '''
    if time_sent < datetime.timestamp(datetime.now()):
        raise InputError(description ="Time sent is a time in the past")
    '''check if the the authorised user has joined the channel'''
    is_joined = False
    for user_in_channel in data['users'][user_id]['user_channel']:
        if channel_id == user_in_channel['channel_id']:
            is_joined = True

    if is_joined == False:
        raise AccessError("authorised user has not joined the channel that he wants to post to")

    '''Implementation'''

    data['messages'].append({'channel_id': channel_id,
                            'message_id': message_id,
                            'u_id': user['u_id'],
                            'message': message,
                            'time_created': time_sent,
                            'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': None}],
                            'is_pinned': False})
    return {'message_id': message_id}

def message_react(token, message_id, react_id):
    data = getData()

    '''Error'''

    '''check if the message_id is valid'''
    message_index = find_message(message_id)
    if message_index == None:
        raise InputError(description = "the message_id is invalid")

    '''check if the react_id is valid'''
    if react_id != 1:
        raise InputError(description = "the react_id is invalid")

    '''check if the user is in the channel to see the message'''
    message_dict = data['messages'][message_index]
    user_id = decode_token(token)
    user_dict = uid_data(user_id)
    channel_id = message_dict['channel_id']
    user_in_channels = user_dict['user_channel']
    is_joined = False
    for channel in user_in_channels:
        if channel['channel_id'] == channel_id:
             is_joined = True

    if is_joined == False and user_dict['permission_id'] == 2:
        raise InputError(description = "user is not in the channel")

    '''check if the user is react for this message'''
    react_list = message_dict['reacts']
    if user_id in react_list[0]['u_ids']:
        raise InputError(description = "the user is react for this message already")

    '''Implementation'''
    react_list[0]['u_ids'].append(user_id)

    return {}

def message_unreact(token, message_id, react_id):
    data = getData()

    '''Error'''

    '''check if the message_id is valid'''
    message_index = find_message(message_id)
    if message_index == None:
        raise InputError(description = "the message_id is invalid")

    '''check if the react_id is valid'''
    if react_id != 1:
        raise InputError(description = "the react_id is invalid")

    '''check if the user is in the channel to see the message'''
    message_dict = data['messages'][message_index]
    user_id = decode_token(token)
    user_dict = uid_data(user_id)
    channel_id = message_dict['channel_id']
    user_in_channels = user_dict['user_channel']
    is_joined = False
    for channel in user_in_channels:
        if channel['channel_id'] == channel_id:
             is_joined = True
    if is_joined == False and user_dict['permission_id'] == 2:
        raise InputError(description = "user is not in the channel")

    '''check if the user is unreact for this message'''
    react_list = message_dict['reacts']
    if user_id not in react_list[0]['u_ids']:
        raise InputError(description = "user is unreact for this message already")

    '''Implementation'''
    react_list[0]['u_ids'].remove(user_id)
    return {}

def message_pin(token, message_id):
    data = getData()
    message_index = find_message(message_id)
    if message_index == None:
        raise InputError(description = "the message_id is invalid")
    message_dict = data['messages'][message_index]

    '''check if the user is in the channel to see the message'''
    user_id = decode_token(token)
    user_dict = uid_data(user_id)
    channel_id = message_dict['channel_id']
    user_in_channels = user_dict['user_channel']
    is_joined = False
    for channel in user_in_channels:
        if channel['channel_id'] == channel_id:
            is_joined = True
    if is_joined == False and user_dict['permission_id'] == 2:
        raise AccessError(description = "user is not in the channel")

    '''check the permission of Authorised user'''
    channel = data['channels'][message_dict['channel_id']]
    u_id = decode_token(token)
    if u_id not in channel['owner_members']: 
        raise InputError(description = "authorised user doesnt have that permission")

    '''check if the message is pinned'''
    if message_dict['is_pinned'] == True:
        raise InputError(description = "the message is pinned")

    '''Implementation'''
    message_dict['is_pinned'] = True
    return {}

def message_unpin(token, message_id):
    data = getData()
    message_index = find_message(message_id)
    '''check if the message_id is valid'''
    if message_index == None:
        raise InputError(description = "the message_id is invalid")
    message_dict = data['messages'][message_index]

    '''check if the user is in the channel to see the message'''
    user_id = decode_token(token)
    user_dict = uid_data(user_id)
    channel_id = message_dict['channel_id']
    user_in_channels = user_dict['user_channel']
    is_joined = False
    for channel in user_in_channels:
        if channel['channel_id'] == channel_id:
             is_joined = True
    if is_joined == False and user_dict['permission_id'] == 2:
        raise AccessError(description = "user isnt in the channel")

    '''check if the message_id is valid'''
    if message_index == None:
        raise InputError(description = "the message_id is invalid")

    '''check the permission of Authorised user'''
    channel = data['channels'][message_dict['channel_id']]
    u_id = decode_token(token)
    if u_id not in channel['owner_members']: 
        raise InputError(description = "authorised user doesnt have that permission")

    '''check if the message is unpinned'''
    if message_dict['is_pinned'] == False:
        raise InputError(description = "message is unpinned")

    '''Implementation'''
    message_dict['is_pinned'] = False
    return {}

def message_remove(token, message_id):
    data = getData()

    '''Error'''

    '''check if the message is already removed'''
    message_index = find_message(message_id)
    if message_index is None:
        raise InputError(description = "message is already removed")

    message_dict = data['messages'][message_index]
    '''check the permission of the authorised user'''
    flag_1 = False
    flag_2 = False
    u_id = decode_token(token)
    user = uid_data(u_id)
    channel = data['channels'][message_dict['channel_id']]
    if message_dict['u_id'] != u_id:
        flag_1 = True
    if (user['permission_id'] != 1) and (u_id not in channel['owner_members']):
        flag_2 = True
    if flag_1 == True and flag_2 == True:
        raise AccessError(description = "authorised user doesnt have that permission")

    '''Implementation'''
    data['messages'].remove(message_dict)
    return {}

def message_edit(token, message_id, message):
    data = getData()

    '''check if the message_id is valid'''
    message_index = find_message(message_id)
    if message_index == None:
        raise InputError(description = "the message_id is invalid")

    message_dict = data['messages'][message_index]
    '''check the permission of the authorised user'''
    flag_1 = True
    flag_2 = True
    u_id = decode_token(token)
    user = uid_data(u_id)
    channel = data['channels'][message_dict['channel_id']]
    if message_dict['u_id'] != u_id:
        flag_1 = False
    if (user['permission_id'] == 2) and (u_id not in channel['owner_members']): 
        flag_2 = False
    if flag_1 == False and flag_2 == False:
        raise AccessError(description = "authorised user doesnt have that permission")

    '''check the length of the message'''
    if len(message) > 1000:
        raise InputError(description = "the message is too long")

    '''Implementation'''
    message_index = find_message(message_id)
    if len(message) == 0:
        message_remove(token, message_id)
    else:
        message_dict['message'] = message
    return {}

def hangman_art(mistakes):
    hangman = ['''
+--+
|   |
|
|
|
|
=======''', '''
+--+
|    |
|   O
|
|
|
=======''', '''
+--+
|    |
|   O
|    |
|
|
=======''', '''
+--+
|    |
|   O
|   /|
|
|
=======''', '''
+--+
|    |
|   O
|   /|\\
|
|
=======''', '''
+--+
|    |
|   O
|   /|\\
|   /
|
=======''', '''
+--+
|    |
|    O
|   /|\\
|   / \\
|
=======''']
    return hangman[mistakes-1]
        
def run_hangman(token, channel_id, data):
    channel = data['channels'][channel_id]
    if channel['hangman']['is_active'] == True:
        return message_send(token, channel_id, "Hangman game is already active")
    word_list = brown.words()
    #randomise a word containing only lowercase letters and between 6-12 in length
    num = randint(0, 1161191)
    word = word_list[num] 
    while len(word) < 6 or len(word) > 12 or word[0].isupper() or word.isalpha() is False:
        num = randint(0, 1161191)        
        word = word_list[num]
    channel['hangman']['word'] = word
    channel['hangman']['is_active'] = True
    channel['hangman']['mistakes'] = 0
    
    #create a list of same length with just underscores
    #to be replaced by correctly guessed characters
    channel['hangman']['guess'].clear()
    for x in range(0, len(word)):
        channel['hangman']['guess'].append("_")

    #create a list for not guessed letters so they can't be guessed again
    channel['hangman']['available'] = "abcdefghijklmnopqrstuvwxyz"
    message_send(token, channel_id, channel['hangman']['guess'])
    
def get_guess(message, token, channel_id, data):
    data = getData
    channel = find_channel(channel_id)
    if channel['hangman']['is_active'] == False:
        return message_send(token, channel_id, "Hangman is currently not active, start a game with /hangman")
    guess = message[7:]
    available = channel['hangman']['available']
    mistakes = channel['hangman']['mistakes']
    word = channel['hangman']['word']     
    guess_list = channel['hangman']['guess']
    if guess.isalpha() is False or len(guess) != 1:
        message_send(token, channel_id, "Invalid input!")
    elif available.find(guess) == -1:
        message_send(token, channel_id, "Letter already guessed!")
    else:
        flag = False
        for x, character in enumerate(word):
            if guess == word[x]:
                guess_list[x] = guess
                flag = True
        if flag == False:
            mistakes += 1
            message_send(token, channel_id, hangman_art(mistakes))
            if mistakes < 7:
                message_send(token, channel_id, "Letter not in word!")        
            channel['hangman']['mistakes'] += 1              
        channel['hangman']['available'].replace(guess, "")
        if mistakes < 7:
            message_send(token, channel_id, guess_list)  
         
    if mistakes == 7:
        message_send(token, channel_id, "You lose! The word was " + word + ".")
        channel['hangman']['is_active'] = False
    if "_" not in guess_list:
        message_send(token, channel_id, word + " was correctly guessed!")
        channel['hangman']['is_active'] = False
