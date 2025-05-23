import os
from os import path
from eventminer import users

users.USERNAMES_PATH = "test_usernames.txt"
users.USERS_PATH = "test_users.csv"
if(path.exists(users.USERNAMES_PATH)): os.remove(users.USERNAMES_PATH)
if(path.exists(users.USERS_PATH)): os.remove(users.USERS_PATH)

def test_get_no_file_usernames():
    saved_error = None
    try:
        usernames = users.get_usernames()
    except Exception as e:
        #should throw error
        saved_error = e
    assert isinstance(saved_error, FileNotFoundError)

def test_get_empty_usernames():
    open(users.USERNAMES_PATH, "w")
    usernames = users.get_usernames()
    #should return empty array
    assert len(usernames) == 0
    os.remove(users.USERNAMES_PATH)

def test_get_usernames():
    file = open(users.USERNAMES_PATH, "w")
    file.write("a\nb")
    file.close()
    usernames = users.get_usernames()
    #should return two names
    assert len(usernames) == 2
    os.remove(users.USERNAMES_PATH)

def test_get_no_file_users():
    users_object = users.get_users()
    assert len(users_object.keys()) == 0

def test_get_empty_file_users():
    open(users.USERS_PATH, "w")
    users_object = users.get_users()
    assert len(users_object.keys()) == 0

def test_get_headers_only_users():
    file = open(users.USERS_PATH, "w")
    file.write(",".join(users.USERS_KEYS) + "\n")
    file.close()
    users_object = users.get_users()
    assert len(users_object.keys()) == 0
    os.remove(users.USERS_PATH)

def test_get_users():
    file = open(users.USERS_PATH, "w")
    file.write(",".join(users.USERS_KEYS) + "\n" + ",".join(["a", "None", "None", "None"]))
    file.close()
    users_object = users.get_users()
    assert len(users_object.keys()) == 1
    assert list(users_object.keys())[0] == "a"
    assert users_object[list(users_object.keys())[0]]["user_id"] == "None"
    os.remove(users.USERS_PATH)

def test_write_empty_users():
    users.USERS = {}
    users.write_users()
    file = open(users.USERS_PATH, 'r', encoding="utf-8")
    assert file.read() == ",".join(users.USERS_KEYS) + "\n"
    file.close()
    os.remove(users.USERS_PATH)

def test_write_users():
    users.USERS = {"a" : dict.fromkeys(users.USERS_KEYS)}
    users.USERS["a"]["username"] = "a"
    users.write_users()
    file = open(users.USERS_PATH, 'r', encoding="utf-8")
    assert file.read() == ",".join(users.USERS_KEYS) + "\n" + "a" + ("," * (len(users.USERS_KEYS)-1))  + "\n"
    file.close()
    os.remove(users.USERS_PATH)
    