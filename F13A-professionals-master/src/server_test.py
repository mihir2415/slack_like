import json
import urllib
import flask # needed for urllib.parse

BASE_URL = 'http://127.0.0.1:3700'
def test_system():
	# Reset
    urllib.request.urlopen(f"{BASE_URL}/workspace/reset")

    data = json.dumps({
	    'email' : 'Hayden@unsw.edu.au',
        'password' : 'TestPassword',
	}).encode('utf-8')

    # payload = json.load(urllib.request.urlopen(f"{BASE_URL}/auth/login"))


    req = urllib.request.Request(f"{BASE_URL}/auth/login", data=data, headers={'Content-Type': 'application/json'})
    payload = json.load(urllib.request.urlopen(req))

    assert payload['email'] == 'Hayden@unsw.edu.au'
    assert payload['password'] == 'TestPassword'
    