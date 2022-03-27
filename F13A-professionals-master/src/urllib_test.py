import json
import urllib
import flask # needed for urllib.parse

BASE_URL = 'http://127.0.0.1:3700'

def do_get_request(data, url):
    queryString = urllib.parse.urlencode(data)
    response = urllib.request.urlopen(f"{BASE_URL}/{url}?{queryString}")
    return json.load(response)
    
def do_post_request(raw_data, url):
    data = json.dumps(raw_data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/{url}", data=data,headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))
    
def do_put_request(raw_data, url):
    data = json.dumps(raw_data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/{url}", data=data,headers={'Content-Type': 'application/json'}, method='PUT')
    return json.load(urllib.request.urlopen(req))  

def test_reset():	
    data = {}
    payload = do_post_request(data, "workspace/reset")

def test_auth_register():
    data = {'email' : 'z5254608@unsw.edu.au', 'password': 'professionals', 'name_first': 'Brent', 'name_last': 'Tonisson'}
    token = do_post_request(data, "auth/register")
    assert "u_id" in token and "token" in token
    
    #test_auth_logout
    data = {'token': token['token']}
    payload = do_post_request(data, "auth/logout")
    assert payload['is_success'] == True
    
    #test_auth_login
    data = {'email' : 'z5254608@unsw.edu.au', 'password': 'professionals'}
    token1 = do_post_request(data, "auth/login")
    assert token1["u_id"] == 0 
    
    #test_channels_create
    data = {'token' : token1['token'], 'name' : 'professionals', 'is_public' : True}
    payload = do_post_request(data, "channels/create")
    assert payload == 0
    
    #create a 2nd user with auth_register
    data = {'email' : 'z5283021@unsw.edu.au', 'password': 'password123', 'name_first': 'Jinyu', 'name_last': 'Yang'}
    token2 = do_post_request(data, "auth/register")
    assert token2["u_id"] == 1 
    
    #create a 2nd channel with 2nd user
    data = {'token' : token2['token'], 'name' : 'F13A', 'is_public' : False}
    payload = do_post_request(data, "channels/create")
    assert payload == 1
    
    #test_channels_listall
    data = {'token': token2['token']}
    payload = do_get_request(data, "channels/listall")
    assert payload == [{'channel_id' : 0, 'name' : 'professionals'}, {'channel_id' : 1, 'name' : 'F13A'}]
    
    #test_channels_list 
    data = {'token': token2['token']}
    payload = do_get_request(data, "channels/list")
    assert payload == [{'channel_id' : 1, 'name' : 'F13A'}]
    
    #test_channel_invite
    data = {'token': token1['token'], 'channel_id': 0, 'u_id': 1}
    payload = do_post_request(data, "channel/invite")
    assert payload == {}
    
    #test_channel_details
    data = {'token': token1['token'], 'channel_id': 0}
    payload = do_get_request(data, "channel/details")
    assert payload == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    
    #test_channel_leave
    data = {'token': token2['token'], 'channel_id': 0}
    payload = do_post_request(data, "channel/leave")
    #run channel details to check user has left channel
    data = {'token': token1['token'], 'channel_id': 0}
    payload = do_get_request(data, "channel/details")
    assert payload == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}]}
    
    #test_channel_join
    data = {'token': token2['token'], 'channel_id': 0}
    payload = do_post_request(data, "channel/join")
    #run channel details to check user has joined channel
    data = {'token': token1['token'], 'channel_id': 0}
    payload = do_get_request(data, "channel/details")
    assert payload == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    
    #test_channel_addowner
    data = {'token': token1['token'], 'channel_id': 0, 'u_id': 1}
    payload = do_post_request(data, "channel/addowner")
    #run channel details to check user is now an owner
    data = {'token': token1['token'], 'channel_id': 0}
    payload = do_get_request(data, "channel/details")
    assert payload == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    
    #test_channel_removeowner
    data = {'token': token1['token'], 'channel_id': 0, 'u_id': 1}
    payload = do_post_request(data, "channel/removeowner")
    #run channel details to check if user's ownership has been removed
    data = {'token': token1['token'], 'channel_id': 0}
    payload = do_get_request(data, "channel/details")
    assert payload == {'name': 'professionals', 'owner_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}], 'all_members': [{'u_id': 0, 'name_first': 'Brent', 'name_last': 'Tonisson'}, {'u_id': 1, 'name_first': 'Jinyu', 'name_last': 'Yang'}]}
    
    #test_user_profile
    data = {'token': token1['token'], 'u_id': 0}
    payload = do_get_request(data, "user/profile")
    assert payload == {'user': {'email': 'z5254608@unsw.edu.au', 'handle_str': 'BrentTonisson', 'name_first': 'Brent', 'name_last': 'Tonisson', 'u_id': 0}}
    
    #test_user_profile_setname
    data = {'token': token1['token'], 'name_first': 'Hayden', 'name_last': 'Smith'}
    payload = do_put_request(data, "user/profile/setname")   
    #test_user_profile_setemail
    data = {'token': token1['token'], 'email': 'z5283022@unsw.edu.au'}
    payload = do_put_request(data, "user/profile/setemail")
    #test_user_profile_sethandle
    data = {'token': token1['token'], 'handle_str': 'haydensmith'}
    payload = do_put_request(data, "user/profile/sethandle")
    #run user_profile to check user's name and email has changed
    data = {'token': token1['token'], 'u_id': 0}
    payload = do_get_request(data, "user/profile")
    assert payload == {'user': {'email': 'z5283022@unsw.edu.au', 'handle_str': 'haydensmith', 'name_first': 'Hayden', 'name_last': 'Smith', 'u_id': 0}}
    
    #test_users_all
    data = {'token': token1['token']}
    payload = do_get_request(data, "users/all")
    assert payload == {'users': [{'user': {'email': 'z5283022@unsw.edu.au', 'handle_str': 'haydensmith', 'name_first': 'Hayden', 'name_last': 'Smith', 'u_id': 0}}, {'user': {'email': 'z5283021@unsw.edu.au', 'handle_str': 'JinyuYang', 'name_first': 'Jinyu', 'name_last': 'Yang', 'u_id': 1}}]}
