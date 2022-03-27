'''
Some user related functions
'''
import os
from io import BytesIO
import requests
from PIL import Image
from data import getData, decode_token, uid_data, get_u_id_list, check_email_valid
from error import InputError
from data import update_profile_image

# pylint: disable=len-as-condition
def user_profile(token, u_id):
    '''For a valid user, returns information about their information'''
    data = getData()
    user_id = decode_token(token)
    if user_id != u_id:
        raise AccessError(description='authorisation is required')
    try:
        user = data['users'][u_id]
    except:
        raise AccessError(description='authorisation is required')
    return {'user':{
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']}}

def user_profile_setname(token, name_first, name_last):
    '''Update the authorised user's first and last name'''
    u_id = decode_token(token)
    user = uid_data(u_id)
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description='first name is invalid')
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description='last name is invalid')
    user['name_first'] = name_first
    user['name_last'] = name_last
    return {}

def user_profile_sethandle(token, handle_str):
    '''Update the authorised user's email address'''
    data = getData()
    u_id = decode_token(token)
    user = uid_data(u_id)
    if len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError(description='handle is invalid')
    is_used = False
    for i in data['users']:
        if i['handle_str'] == handle_str:
            is_used = True
    if is_used:
        raise InputError(description='handle is occupied')
    user['handle_str'] = handle_str
    return {}

def user_profile_setemail(token, email):
    '''Update the authorised user's handle (i.e. display name)'''
    data = getData()
    u_id = decode_token(token)
    user = uid_data(u_id)
    if not check_email_valid(email):
        raise InputError(description='email is invalid')
    is_used = False
    for i in data['users']:
        if i['email'] == email:
            is_used = True
    if is_used:
        raise InputError(description='email is occupied')
    user['email'] = email
    return {}

def users_all(token):
    '''Returns a list of all users and their associated details'''
    select_users = []
    uid_list = get_u_id_list()
    for uid in uid_list:
        select_users.append(user_profile(token, uid))
    return {'users':select_users}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Update the authorised user's photo (avatar)
    '''
    # ensures the token passed is valid
    u_id = decode_token(token)

    # Download image from img_url
    try:
        response = requests.get(img_url)
    except:
        raise InputError(description="Unable to fetch the img URL")

    # Check the correct response code is present
    if response.status_code != 200:
        raise InputError(description="Image request error")

    img = Image.open(BytesIO(response.content))

    # Check the format of the image
    if img.format != 'JPEG':
        raise InputError(description="Image not JPG")

    width, height = img.size

    x_start = int(x_start)
    x_end = int(x_end)
    y_start = int(y_start)
    y_end = int(y_end)

    # Crop and store the image
    try:
        cropped_img = img.crop((x_start, y_start, x_end, y_end))
    except:
        raise InputError(description='Image dimesions error')

    
    os.makedirs("./imgurl")

    location = "imgurl/" + 'avatar_' + str(u_id) + ".jpg"
    img_name = 'avatar_' + str(u_id) + ".jpg"
    cropped_img.save(f'./{location}')
    
    # Generates URL
    url = f'http://localhost:3700/imgurl/{img_name}.jpg'

    # Update the user's image in the DB
    update_profile_image(url, u_id)

    return {}
