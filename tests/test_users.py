import os
from os import path
from eventminer.users import Users

def cleanup():
    Users.USERS = {}
    Users.USERNAMES_PATH = "test_usernames.txt"
    Users.USERS_PATH = "test_users.csv"
    if(path.exists(Users.USERNAMES_PATH)): os.remove(Users.USERNAMES_PATH)
    if(path.exists(Users.USERS_PATH)): os.remove(Users.USERS_PATH)

cleanup()

def test_get_no_file_usernames():
    assert path.exists(Users.USERNAMES_PATH) == False, "Usernames TXT should not exist before mining."

    saved_error = None
    try:
        usernames = Users.get_usernames()
    except Exception as e:
        #should throw error
        saved_error = e
    assert isinstance(saved_error, FileNotFoundError)
    cleanup()

def test_get_empty_usernames():
    assert path.exists(Users.USERNAMES_PATH) == False, "Usernames TXT should not exist before mining."
    open(Users.USERNAMES_PATH, "w")
    usernames = Users.get_usernames()
    #should return empty array
    assert len(usernames) == 0
    cleanup()

def test_get_usernames():
    assert path.exists(Users.USERNAMES_PATH) == False, "Usernames TXT should not exist before mining."
    file = open(Users.USERNAMES_PATH, "w")
    file.write("a\nb")
    file.close()
    usernames = Users.get_usernames()
    #should return two names
    assert len(usernames) == 2
    cleanup()

def test_get_no_file_users():
    users_object = Users.get_users()
    assert len(users_object.keys()) == 0
    cleanup()

def test_get_empty_file_users():
    assert path.exists(Users.USERS_PATH) == False, "User CSV should not exist before mining."

    open(Users.USERS_PATH, "w")
    users_object = Users.get_users()
    assert len(users_object.keys()) == 0
    cleanup()

def test_get_headers_only_users():
    assert path.exists(Users.USERS_PATH) == False, "User CSV should not exist before mining."

    file = open(Users.USERS_PATH, "w")
    file.write(",".join(Users.USERS_KEYS) + "\n")
    file.close()
    users_object = Users.get_users()
    assert len(users_object.keys()) == 0
    cleanup()

def test_get_users():
    assert path.exists(Users.USERS_PATH) == False, "User CSV should not exist before mining."

    file = open(Users.USERS_PATH, "w")
    file.write(",".join(Users.USERS_KEYS) + "\n" + ",".join(["a", "None", "None", "None"]))
    file.close()
    users_object = Users.get_users()
    assert len(users_object.keys()) == 1
    assert list(users_object.keys())[0] == "a"
    assert users_object[list(users_object.keys())[0]]["user_id"] == "None"
    cleanup()

def test_write_empty_users():
    assert path.exists(Users.USERS_PATH) == False, "User CSV should not exist before mining."

    Users.USERS = {}
    Users.write_users()
    file = open(Users.USERS_PATH, 'r', encoding="utf-8")
    assert file.read() == ",".join(Users.USERS_KEYS) + "\n"
    file.close()
    cleanup()

def test_write_users():
    assert path.exists(Users.USERS_PATH) == False, "User CSV should not exist before mining."
    
    Users.USERS = {"a" : dict.fromkeys(Users.USERS_KEYS)}
    Users.USERS["a"]["username"] = "a"
    Users.write_users()
    file = open(Users.USERS_PATH, 'r', encoding="utf-8")
    assert file.read() == ",".join(Users.USERS_KEYS) + "\n" + "a" + ("," * (len(Users.USERS_KEYS)-1))  + "\n"
    file.close()
    cleanup()
    