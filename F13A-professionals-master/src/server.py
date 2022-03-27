import sys
import threading
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from data import *
from auth import auth_login, auth_logout, auth_register, password_reset_request, password_reset
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from message import message_send, message_sendlater, message_react, message_unreact, message_pin, message_unpin, message_remove, message_edit
from user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname, users_all, user_profile_uploadphoto
from search import *
from standup import start_standup, active_standup, send_standup
from admin import admin_permission_change, workspace_reset

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

'''
auth_stuff
'''

@APP.route("/auth/login", methods=['POST'])
def login():
    '''input: email, password'''
    data = request.get_json()
    result = auth_login(data['email'], data['password'])
    return dumps(result)

@APP.route("/auth/logout", methods=['POST'])
def logout():
    '''input: token'''
    data = request.get_json()
    result = auth_logout(data['token'])
    return dumps(result)

@APP.route("/auth/register", methods=['POST'])
def register():
    '''input: email, password, name_first, name_last'''
    data = request.get_json()
    result = auth_register(data['email'],
                           data['password'],
                           data['name_first'],
                           data['name_last'])
    return dumps(result)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def reset_request():
    '''input: email'''
    data = request.get_json()
    result = password_reset_request(data['email'])
    return dumps(result)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def reset():
    '''input: reset_code, new_password'''
    data = request.get_json()
    result = password_reset(data['reset_code'], data['new_password'])
    return dumps(result)

'''
channel_stuff
'''
@APP.route("/channel/invite", methods=['POST'])
def invite():
    '''input:token, channel_id, u_id'''
    data = request.get_json()
    result = channel_invite(data['token'],
                            data['channel_id'],
                            data['u_id'])
    return dumps(result)
    
@APP.route("/channel/details", methods=['GET'])
def details():
    '''input:token, channel_id, message'''
    result = channel_details(request.args.get('token'),
                             request.args.get('channel_id'))
    return dumps(result)

@APP.route("/channel/messages", methods=['GET'])
def messages():
    '''input:token, channel_id, start'''
    result = channel_messages(request.args.get('token'),
                              request.args.get('channel_id'),
                              request.args.get('start'))
    return dumps(result)
    
@APP.route("/channel/leave", methods=['POST'])
def leave():
    '''input:token, channel_id,'''
    data = request.get_json()
    result = channel_leave(data['token'],
                           data['channel_id'])
    return dumps(result)
    
@APP.route("/channel/join", methods=['POST'])
def join():
    '''input:token, channel_id,'''
    data = request.get_json()
    result = channel_join(data['token'],
                          data['channel_id'])
    return dumps(result)
    
@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    '''input:token, channel_id, u_id'''
    data = request.get_json()
    result = channel_addowner(data['token'],
                              data['channel_id'],
                              data['u_id'])
    return dumps(result)
    
@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    '''input:token, channel_id, u_id'''
    data = request.get_json()
    result = channel_removeowner(data['token'],
                                 data['channel_id'],
                                 data['u_id'])
    return dumps(result)

'''
channels stuff
'''
@APP.route("/channels/list", methods=['GET'])
def list_channels():
    '''input:token'''
    result = channels_list(request.args.get('token'))
    return dumps(result)
    
@APP.route("/channels/listall", methods=['GET'])
def listall_channels():
    '''input:token, channel_id, u_id'''
    result = channels_listall(request.args.get('token'))
    return dumps(result)

@APP.route("/channels/create", methods=['POST'])
def create_channel():
    '''input:token, name, is_public'''
    data = request.get_json()
    result = channels_create(data['token'],
                             data['name'],
                             data['is_public'])
    return dumps(result)

'''
message_stuff
'''
@APP.route("/message/send", methods=['POST'])
def send():
    '''input:token, channel_id, message'''
    data = request.get_json()
    result = message_send(data['token'],
                          data['channel_id'],
                          data['message'])
    return dumps(result)

@APP.route("/message/sendlater", methods=['POST'])
def sendlater():
    '''input:token, message_id, react_id, time_sent'''
    data = request.get_json()
    result = message_sendlater(data['token'],
                               data['channel_id'],
                               data['message'],
                               data['time_sent'])
    return dumps(result)

@APP.route("/message/react", methods=['POST'])
def react():
    '''input:token, message_id, react_id'''
    data = request.get_json()
    result = message_react(data['token'],
                           data['message_id'],
                           data['react_id'])
    return dumps(result)

@APP.route("/message/unreact", methods=['POST'])
def unreact():
    '''input:token, message_id, react_id'''
    data = request.get_json()
    result = message_unreact(data['token'],
                             data['message_id'],
                             data['react_id'])
    return dumps(result)

@APP.route("/message/pin", methods=['POST'])
def pin():
    '''input:token, message_id'''
    data = request.get_json()
    result = message_pin(data['token'], data['message_id'])
    return dumps(result)

@APP.route("/message/unpin", methods=['POST'])
def unpin():
    '''input:token, message_id'''
    data = request.get_json()
    result = message_unpin(data['token'], data['message_id'])
    return dumps(result)

@APP.route("/message/remove", methods=['DELETE'])
def remove():
    '''input:token, message_id'''
    data = request.get_json()
    result = message_remove(data['token'], data['message_id'])
    return dumps(result)

@APP.route("/message/edit", methods=['PUT'])
def edit():
    '''input:token, message_id, message'''
    data = request.get_json()
    result = message_edit(data['token'],
                          data['message_id'], 
                          data['message'])
    return dumps(result)

'''
user_stuff
'''

@APP.route("/user/profile", methods=['GET'])
def profile():
    '''input: token, u_id'''
    result = user_profile(request.args.get('token'),
                          int(request.args.get('u_id')))
    return dumps(result)

@APP.route("/user/profile/setname", methods=['PUT'])
def setname():
    '''input:token, name_first, name_last'''
    data = request.get_json()
    result = user_profile_setname(data['token'],
                                  data['name_first'],
                                  data['name_last'])
    return dumps(result)

@APP.route("/user/profile/setemail", methods=['PUT'])
def setemail():
    '''input:token, email'''
    data = request.get_json()
    result = user_profile_setemail(data['token'],data['email'])
    return dumps(result)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle():
    '''input:token, handle_str'''
    data = request.get_json()
    result = user_profile_sethandle(data['token'], data['handle_str'])
    return dumps(result)

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def user_profile_photo():
    '''
    Handles the requests for the /user/profile/uploadphoto route.
    '''
    data = request.get_json()

    token = data['token']
    img_url = data['img_url']
    x_start = data['x_start']
    y_start = data['y_start']
    x_end = data['x_end']
    y_end = data['y_end']

    return dumps(user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end))

@APP.route("/users/all", methods=['GET'])
def all_users():
    '''input:token'''
    result = users_all(request.args.get('token'))
    return dumps(result)
    
'''
search
'''
@APP.route("/search", methods=['GET'])
def search_message():
    '''input: token, query_str'''
    result = search(request.args.get('token'),
                    request.args.get('query_str'))
    return dumps(result)

'''
standup
'''
@APP.route("/standup/start", methods=['POST'])
def start_standup():
    '''input: token, channel_id, length'''
    data = request.get_json()
    result = standup_start(data['token'], 
                           data['channel_id'],
                           data['length'])
    return dumps(result)
    
@APP.route("/standup/active", methods=['GET'])
def standup_active():
    '''input: token, channel_id'''
    result = active_standup(request.args.get('token'),
                           request.args.get('channel_id'))
    return dumps(result)

@APP.route("/standup/send", methods=['POST'])
def send_standup():
    '''input: token, channel_id, message'''
    data = request.get_json()
    result = standup_send(data['token'], 
                           data['channel_id'],
                           data['message'])
    return dumps(result)

'''
admin
'''
@APP.route("/admin/userpermission/change", methods=['POST'])    
def permission():
    '''input:token, u_id, permission_id'''
    data = request.get_json()
    result = admin_permissionChange(data['token'],
                                    data['u_id'],
                                    data['permission_id'])
    return dumps(result)

@APP.route("/admin/user/remove", methods=['DELETE'])    
def admin_remove():
    '''input:token, u_id'''
    data = request.get_json()
    result = admin_user_remove(data['token'], data['u_id'])
    return dumps(result)
    
'''
workspace
'''
@APP.route("/workspace/reset", methods=['POST'])    
def reset_workspace():
    '''input:'''
    result = workspace_reset()
    return dumps(result)
    
if __name__ == "__main__":
    workspace_reset()
    establish_data()
    threading.Thread(target=lambda: time_interval(5)).start()
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8000))
    

