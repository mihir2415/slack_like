from nltk.corpus import brown
from random import randint
from data import getData

def hangman_art(mistakes):
    hangman = ['''
+---+
|   |
|
|
|
|
=======''', '''
+---+
|   |
|   O
|
|
|
=======''', '''
+---+
|   |
|   O
|   |
|
|
=======''', '''
+---+
|   |
|   O
|  /|
|
|
=======''', '''
+---+
|   |
|   O
|  /|\\
|
|
=======''', '''
+---+
|   |
|   O
|  /|\\
|  /
|
=======''', '''
+---+
|   |
|   O
|  /|\\
|  / \\
|
=======''']
    return hangman[mistakes-1]
        
def run_hangman(token, channel_id):
    data = getData()
    channel = data['channels'][channel_id]
    if channel['hangman']['is_active'] == True:
        return send_message(token, channel_id, "Hangman game is already active")
    word_list = brown.words()
    channel['hangman']['is_active'] == True
    #randomise a word containing only lowercase letters and between 6-12 in length
    num = randint(0, 1161191)
    word = word_list[num] 
    while len(word) < 6 or len(word) > 12 or word[0].isupper() or word.isalpha() is False:
        num = randint(0, 1161191)        
        word = word_list[num]
    channel['hangman']['word'] = word
    
    #create a list of same length with just underscores
    #to be replaced by correctly guessed characters
    guess_list = []
    for x in range(0, len(word)):
        guess_list.append("_")
    channel['hangman']['guess'] == str(guess_list)

    #create a list for not guessed letters so they can't be guessed again
    available = "abcdefghijklmnopqrstuvwxyz"
    message_send(token, channel_id, guess_list)
    message_send(token, channel_id, "available letters are " + available)
    #print(word) Disabled to hide the word
    
def get_guess(message, token, channel_id):
    data = getData
    channel = data['channels'][channel_id]
    if channel['hangman']['is_active'] == False:
        return message_send(token, channel_id, "Hangman is currently not active, start a game with /hangman")
    guess == message[7:]
    mistakes = channel['hangman']['mistakes']
    word = channel['hangman']['word']
    guess_list = channel['hangman']['guess']
    if mistakes < 7 and "_" in guess_list:
        message_send(token, channel_id, guess_list)
        message_send(token, channel_id, "available letters are " + available)
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
                message_send(token, channel_id, "Letter not in word!")        
                mistakes += 1
                message_send(token, channel_id, hangman_art(mistakes))
            available = available.replace(guess, "")
        
    if mistakes == 7:
        message_send(token, channel_id, "You lose! The word was " + word + ".")
    else:
        message_send(token, channel_id, word + " was correctly guessed!")
    channel['hangman']['mistakes'] = 0
    channel['hangman']['is_active'] == False
