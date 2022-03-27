

Assumptions for Auth.py:

    We assume that emails for auth_login will have some max character limit i.e. 128 characters.
<<<<<<< HEAD
    
    We assume that emails, passwords, first names, last names and tokens will only contain ASCII characters.
    
=======

    We assume that emails for auth_login will only contain ASCII characters.

>>>>>>> mihir_first_branch
    The Assignment spec states in the section on auth_register:
        "A handle is generated that is the concatenation of a lowercase-only first name and last name"
    We assume that if the user enters uppercase charachters, no error is thrown, and that to produce
    the concatenation, any uppercase characters are simply converted to lower case characters.

    We assume that a password can contain regular ascii characters (include spaces), but cannot be empty.

    We assume that an email address can only contain one @ symbol (i.e. the string on each side of the @
    cannot contain any @ symbols.)

<<<<<<< HEAD
    We assume that in auth_register, the requirement of both first names and lasts names being
        "between 1 and 50 characters in length"
    is inclusive of both 1 and 50 so that strings of those lengths are also valid.

    We assume that users can have the same first and last name and password. i.e. only emails clashing will
    throw and error upon registration.

    We assume that the active token given to auth_logout is the token produced on login, not on account registration.
    
=======
>>>>>>> mihir_first_branch
Assumptions for channels.py:

    We assume that once user create a channel, user is immediately added to the channel he create.

    We assume that 'channels_list' and 'channels_listall' will work normally if there is no channel.

    We assume that, when call the function 'channels_listall', user can see the channels which are 'Public' or the channels which the user included.
<<<<<<< HEAD
    
    We assume that channel can't be created if the channel_name already existes (Input error)
    
    We assume that channel can't be created if the channel_name is empty (Input error)
=======

    We assume that channel can't be created if the channel_name is existed
>>>>>>> mihir_first_branch

Assumptions for message.py:
    
    We assume that the first people who register an account of Slackr is the owner of Slackr.(!)
    
    We assume that the owner of Slackr can send, edit and remove a message for a channel no matter he is in that channel or not.
    
    We assume that nothing happens when 'message' from 'message_edit' is the same as the target message. 
    
    We assume that message can't be empty when calling any functions from message.py


Assumptions for other.py

We assume that the data is stored in the order of the input

We assume that the other functions are working correctly

Assumptions for user.py:

We assume that the user_id starts from 1
    
Assumptions for channel.py:

<<<<<<< HEAD
    We assume that a user can not be invited to a channel if they are already in it.
    
    We assume that for all functions, unless otherwise stated, the Channel ID provided is valid.
    
    We assume that for all functions, unless otherwise stated, the User ID provided is valid.
    
    We assume that message can't be empty when calling any functions from channel.py.
    
    We assume that channel can not be left if user is not in the channel already.
    
    We assume owner can only be added if they are in the channel and not already an owner.
    
    We assume owner can only be removed if they are already an owner of the channel.
    
    We assume that message can't be empty when calling any functions from message.py (Input error)
=======
    We assume that nothing happens when 'message' from 'message_edit' is the same as the target message.

Assumptions for other.py

    We assume that the data is stored in the order of the input

    We assume that the other functions are working correctly

Assumptions for user.py

    We assume that the user_id starts from 1
>>>>>>> mihir_first_branch
