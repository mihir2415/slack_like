'''
test for user
'''
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=unidiomatic-typecheck
# pylint: disable=unused-variable
import pytest
from admin import workspace_reset
from auth import auth_register
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from error import InputError

def test_user_profile():
    '''
    all tests for user_profile
    '''
    workspace_reset()
    user_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
    user_2 = auth_register("hayden@usyd.com", "securitystring2", "Hayden", "Jordan")
    user_3 = auth_register("hayden@uts.com", "securitystring3", "Hayden", "Coles")

    # Storing user profiles in user_prof_(Num)

    user_prof_1 = user_profile(user_1['token'], user_1['u_id'])
    user_prof_2 = user_profile(user_1['token'], user_2['u_id'])
    user_prof_2_copy = user_profile(user_2['token'], user_2['u_id'])

    # Assuming that when generating u_ids, the numbering starts from 0
    # Checking for invalid u_ids which must raise an InputError
    # Even if the u_id given is greater than the number of users, it must raise an errors

    with pytest.raises(InputError):
        user_profile(user_1['token'], 9)
    # Some more invalid cases to consider
    with pytest.raises(InputError):
        user_profile(user_1['token'], 'string')
    with pytest.raises(InputError):
        user_profile(user_1['token'], 8.1)

    # Checking that the types of all elements in user_profile_1 are correct
    assert type(user_prof_1) == dict
    assert type(user_prof_1['user']['u_id']) == int
    assert type(user_prof_1['user']['email']) == str
    assert type(user_prof_1['user']['name_first']) == str
    assert type(user_prof_1['user']['name_last']) == str
    assert type(user_prof_1['user']['handle_str']) == str

def test_user_profile_setname():
    '''
    all tests for user_profile_setname
    '''
    workspace_reset()
    user_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")

    user_prof_1 = user_profile(user_1['token'], user_1['u_id'])

    # The program must raise an exception if the last or the first name in graeter than 50 characters
    # or less than 1

    # Raises an input error when the first name is greater than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(user_1['token'], 60*'b', user_prof_1['user']['name_last'])
    # Raises an input error when the first name is less than 1 character
    with pytest.raises(InputError):
        user_profile_setname(user_1['token'], '', user_prof_1['user']['name_last'])
    # Raises an input error when the last name is greater than 50 characters
    with pytest.raises(InputError):
        user_profile_setname(user_1['token'], user_prof_1['user']['name_first'], 60*'b')
    # Raises an input error when the last name is less than 1 character
    with pytest.raises(InputError):
        user_profile_setname(user_1['token'], user_prof_1['user']['name_first'], '')

    # Changing the name to something else to test
    user_profile_setname(user_1['token'], 'Something', 'Else')
    # Updating the user profile
    user_prof_1 = user_profile(user_1['token'], user_1['u_id'])

    assert user_prof_1['user']['name_first'] == 'Something'
    assert user_prof_1['user']['name_last'] == 'Else'

def test_user_profil_setemail():
    '''
    all tests for user_profile_setemail
    '''
    workspace_reset()
    user_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
    fake_email_1 = 'rushil.212'
    fake_email_2 = 'mihir.com'
    fake_email_3 = 'professionals@com'

    with pytest.raises(InputError) as e:
        user_profile_setemail(user_1['token'], fake_email_1)

    with pytest.raises(InputError) as e:
        user_profile_setemail(user_1['token'], fake_email_2)

    with pytest.raises(InputError) as e:
        user_profile_setemail(user_1['token'], fake_email_3)

    user_2 = auth_register("haydencoolboy@unsw.com", "securitystring2", "Hayden", "Jordan")
     #This raises an error because the Email ID is being used by another user.
    with pytest.raises(InputError) as e:
        user_profile_setemail(user_2['token'], "hayden@unsw.com")

def test_user_profile_sethandle():
    '''
    all tests for user_profile_setemail
    '''
    workspace_reset()
    user_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")

    sample_string_1 = 'a'*24
    sample_string_2 = 'b'

     #Should raise an error as the string 'a' is of length 2.
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_1['token'], sample_string_2)

    #Should raise an error as the string b is of length 24.
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_1['token'], sample_string_1)

    user_profile_sethandle(user_1['token'], 'DavidPhillips')


    user_2 = auth_register('hello123@real.com', 'securitystring2', 'Marcos', 'Alonso')
    #This raises an error because the handle string is being used by another user.
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_2['token'], 'DavidPhillips')
