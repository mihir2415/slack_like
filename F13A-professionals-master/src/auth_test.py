"""
Tests for auth_login.
"""

#pylint: disable=unused-variable

import pytest
from auth import auth_login, auth_logout, auth_register, password_reset_request, password_reset
from error import InputError
from admin import workspace_reset
from data import getData

def test_login():
    """
    Tests a normal login to check that the u_id is correctly returned.
    """
    workspace_reset()
    auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
    assert auth_login("hayden@unsw.com", "securitystring")['u_id'] == 0

def test_invalid_email_1():
    """
    Tests an invalid email login that has too many @ symbols.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_login("hayden@hayden@unsw.com", "password")

def test_invalid_email_2():
    """
    Tests an invalid email login that has nothing following the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("hayden.unsw@", "password")

def test_invalid_email_3():
    """
    Tests an invalid email login that has nothing before the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("@hayden.unsw", "password")

def test_invalid_email_4():
    """
    Tests an invalid email login that has a non-ascii character.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("Ø@unsw", "password")

def test_invalid_email_5():
    """
    Tests an invalid email login that has no @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("hayden.unsw", "password")

def test_invalid_email_6():
    """
    Tests an invalid email login that has nothing before or after the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("@", "password")

def test_invalid_email_7():
    """
    Tests an invalid email login that has too many @ symbols.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("@@@@", "password")

def test_invalid_password():
    """
    Tests an invalid password login that has non ascii characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("Hayden@unsw.com", "ØØØ")

def test_no_email():
    """
    Tests an invalid email login that has no email.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("", "securitystring")

def test_incorrect_email():
    """
    Tests an invalid email login that uses an incorrect email.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("incorrect@email.com", "securitystring")

def test_unregistered_email():
    """
    Tests an invalid email login that uses an incorrect email.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
        auth_register("James@unsw.com", "securitystring2", "James", "Smith")
        auth_register("Owen@unsw.com", "securitystring3", "Owen", "Smith")
        auth_register("Kayla@unsw.com", "securitystring4", "Kayla", "Smith")
        auth_login("hayden@USYD.com", "password")

def test_no_password():
    """
    Tests an invalid password login that uses no password.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("hayden@unsw.com", "")

def test_incorrect_password():
    """
    Tests an invalid password login that uses an incorrect password.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
        auth_login("hayden@unsw.com", "incorrectpassword")

def test_correct_login():
    """
    Tests a successful login
    """
    workspace_reset()
    user_id = auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")['u_id']
    login_user_id = auth_login("hayden@unsw.com", "securitystring")['u_id']
    assert user_id == login_user_id

def test_correct_login_2():
    """
    Tests a successful login with multiple users registered.
    """
    workspace_reset()
    user_id_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")['u_id']
    user_id_2 = auth_register("James@unsw.com", "securitystring2", "James", "Smith")['u_id']
    user_id_3 = auth_register("Owen@unsw.com", "securitystring3", "Owen", "Smith")['u_id']
    user_id_4 = auth_register("Kayla@unsw.com", "securitystring4", "Kayla", "Smith")['u_id']
    login_user_id = auth_login("hayden@unsw.com", "securitystring1")['u_id']
    assert user_id_1 == login_user_id

def test_multi_login():
    """
    Tests a successful login for multiple users that are registered.
    """
    workspace_reset()
    auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")
    auth_register("James@unsw.com", "securitystring2", "James", "Dunn")
    assert auth_login("hayden@unsw.com", "securitystring")
    assert auth_login("James@unsw.com", "securitystring2")

#Tests for auth_logout:

def test_logout():
    """
    Tests a successful logout.
    """
    workspace_reset()
    init_token = auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")['token']
    assert auth_logout(init_token)['is_success']

def test_logout_2():
    """
    Tests a successful logout with multiple registered users.
    """
    workspace_reset()
    init_token = auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")['token']
    init_token_2 = auth_register("James@unsw.com", "securitystring2", "James", "Dunn")['token']
    login_token = auth_login("hayden@unsw.com", "securitystring")['token']
    login_token_2 = auth_login("James@unsw.com", "securitystring2")['token']
    assert auth_logout(login_token)['is_success']

def test_multi_logout():
    """
    Tests a successful logout for multiple users that are registered.
    """
    workspace_reset()
    init_token = auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")['token']
    init_token_2 = auth_register("James@unsw.com", "securitystring2", "James", "Dunn")['token']
    login_token = auth_login("hayden@unsw.com", "securitystring")['token']
    login_token_2 = auth_login("James@unsw.com", "securitystring2")['token']
    assert auth_logout(login_token)['is_success']
    assert auth_logout(login_token_2)['is_success']




#Tests for auth_register:


def test_register():
    """
    Tests a successful user registration.
    """
    workspace_reset()
    assert auth_register("hayden@unsw.com", "securitystring", "Hayden", "Smith")

def test_invalid_email_1a():
    """
    Tests an invalid email user registration that has too many @ symbols.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@hayden@unsw.com", "securitystring", "Hayden", "Smith")

def test_invalid_email_2a():
    """
    Tests an invalid email user registration that has nothing after the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden.unsw@", "securitystring", "Hayden", "Smith")

def test_invalid_email_3a():
    """
    Tests an invalid email user registration that has nothing before the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("@hayden.unsw", "securitystring", "Hayden", "Smith")

def test_invalid_email_4a():
    """
    Tests an invalid email user registration that has a non ascii character.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("Ø@unsw", "securitystring", "Hayden", "Smith")

def test_invalid_email_5a():
    """
    Tests an invalid email user registration that has no @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden.unsw", "securitystring", "Hayden", "Smith")

def test_invalid_email_6a():
    """
    Tests an invalid email user registration that has nothing before or after the @ symbol.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("@", "securitystring", "Hayden", "Smith")

def test_invalid_email_7a():
    """
    Tests an invalid email user registration that has too many @ symbols.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("@@@@", "securitystring", "Hayden", "Smith")

def test_invalid_password_1():
    """
    Tests an invalid password user registration that has too few characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "hi", "Hayden", "Smith")

def test_invalid_fname_1():
    """
    Tests an invalid name user registration that has too few characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "", "Smith")

def test_invalid_fname_2():
    """
    Tests an invalid name user registration that has too many characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("h@unsw", "pw123", "HaydenHaydenHaydenHaydenHaydenHaydenHaydenHaydenHayden",
                      "Smith")

def test_invalid_lname_1():
    """
    Tests an invalid name user registration that has too few characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden", "")

def test_invalid_lname_2():
    """
    Tests an invalid name user registration that has too many characters.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring", "Hayden",
                      "SmithSmithSmithSmithSmithSmithSmithSmithSmithSmithSmith")

def test_occupied_email():
    """
    Tests an invalid registration that has users an occupied email address.
    """
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")
        auth_register("hayden@unsw.com", "securitystring2", "Hayden", "Brown")

def test_multiple_registrations():
    """
    Tests unique u_id given for different user registrations.
    """
    workspace_reset()
    user_id_1 = auth_register("hayden@unsw.com", "securitystring1", "Hayden", "Smith")['u_id']
    user_id_2 = auth_register("james@unsw.com", "securitystring2", "James", "Brown")['u_id']
    assert user_id_1 != user_id_2

def test_twin_password():
    """
    Tests multiple registration success even with matching passwords.
    """
    workspace_reset()
    user_id_1 = auth_register("hayden1@unsw.com", "securitystring", "Hayden", "Smith")['u_id']
    user_id_2 = auth_register("Larry@unsw.com", "securitystring", "Larry", "Green")['u_id']
    assert user_id_1 != user_id_2

def test_twin_profile():
    """
    Tests unique u_id given for different user registrations with similar details.
    """
    workspace_reset()
    user_id_1 = auth_register("hayden1@unsw.com", "securitystring", "Hayden", "Smith")['u_id']
    user_id_2 = auth_register("hayden2@unsw.com", "securitystring", "Hayden", "Smith")['u_id']
    assert user_id_1 != user_id_2


#Tests for password_reset functions:

def test_password_reset():
    '''
    Tests the email sending functionality of a password reset attempt.
    '''
    workspace_reset()
    temp_data = getData()
    user_id_1 = auth_register("z5255355@ad.unsw.edu.au", "test123", "Ethan", "Soussa")['u_id']
    password_reset_request("z5255355@ad.unsw.edu.au")

    for user in temp_data['users']:
        if user['u_id'] == user_id_1:
            reset_user = user

    assert reset_user['reset_code'] is not None
    assert reset_user['password'] == "test123"

    password_reset(reset_user['reset_code'], "new_password123")

    assert reset_user['reset_code'] is None
    assert reset_user['password'] == "new_password123"

def test_password_reset_failure():
    '''
    Tests the email sending functionality of a password reset attempt with invalid inputs.
    '''
    workspace_reset()
    temp_data = getData()
    user_id_1 = auth_register("z5255355@ad.unsw.edu.au", "test123", "Ethan", "Soussa")['u_id']
    user_id_2 = auth_register("hayden2@unsw.com", "securitystring", "Hayden", "Smith")['u_id']


    with pytest.raises(InputError):
        password_reset_request("HSmith@ad.unsw.edu.au")

    password_reset_request("z5255355@ad.unsw.edu.au")

    for user in temp_data['users']:
        if user['u_id'] == user_id_1:
            reset_user = user

    with pytest.raises(InputError):
        password_reset('incorrect_code', "new_password123")
        password_reset(None, "new_password123")
        password_reset(reset_user['reset_code'], "")


    password_reset(reset_user['reset_code'], "new_password123")

    assert reset_user['reset_code'] is None
    assert reset_user['password'] == "new_password123"
