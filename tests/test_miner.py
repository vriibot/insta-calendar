import eventminer
from eventminer.posts import Posts
import os
from os import path
import pytest
import shutil

def cleanup():
    Posts.POSTS = {}
    Posts.EVENT_DATES = []
    eventminer.miner.LOGIN = False
    Posts.IMAGE_DIR = "testimages"
    Posts.POSTS_PATH = "test_posts.csv"
    eventminer.users.USERS_PATH = "test_users.csv"
    eventminer.users.USERNAMES_PATH = "test_usernames.txt"
    if(path.exists(eventminer.users.USERS_PATH)): os.remove(eventminer.users.USERS_PATH)
    if(path.exists(eventminer.users.USERNAMES_PATH)): os.remove(eventminer.users.USERNAMES_PATH)
    if(path.exists(Posts.POSTS_PATH )): os.remove(Posts.POSTS_PATH)
    if(path.exists(Posts.IMAGE_DIR)): shutil.rmtree(Posts.IMAGE_DIR, True)

cleanup()

# @pytest.fixture(autouse=True)
# def setup(monkeypatch):
#     monkeypatch.setattr(posts, "IMAGE_DIR", "testimages")
#     monkeypatch.setattr(posts, "POSTS_PATH", "test_posts.csv")

# def test_no_session_login(monkeypatch):
#     monkeypatch.setattr(credentials, "SESSION_PATH", "test_session.json")
#     miner.LOGIN = False
#     try:
#         miner.login()
#     except Exception:
#         assert False
#     assert miner.LOGIN == True
#     os.remove(credentials.SESSION_PATH)

def test_login():
    assert eventminer.miner.LOGIN == False, "Should not be logged in before login attempt."

    eventminer.credentials.load_credentials()
    # try:
    eventminer.miner.login()
    # except Exception:
    #     assert False
    assert eventminer.miner.LOGIN == True
    cleanup()

def test_mine_bad_user():
    username = "a"
    user_data = eventminer.miner.mine_user(username, {})
    assert len(list(user_data.keys())) == 0
    cleanup()

def test_mine_post():
    assert path.exists(Posts.POSTS_PATH) == False, "Posts CSV should not exist before mining."

    eventminer.credentials.load_credentials()
    eventminer.miner.login()
    eventminer.miner.mine_post("https://www.instagram.com/p/DKq-UpRSF-1/")
    posts_csv = open(Posts.POSTS_PATH).readlines()

    # added to postcsv and created image
    assert len(posts_csv) == 2
    assert path.exists(Posts.IMAGE_DIR + "/DKq-UpRSF-1.jpg")

    #clean up
    cleanup()

def test_mine_post_force_same_date():
    assert path.exists(Posts.POSTS_PATH) == False, "Posts CSV should not exist before mining."

    eventminer.credentials.load_credentials()
    eventminer.miner.login()

    #setup existing event
    posts_csv = open(Posts.POSTS_PATH, "w")
    posts_csv.write("\t".join(Posts.POSTS_KEYS) + "\n" + '''00_00	instacalendar_test	2025-06-09T07:21:19+00:00	2025-06-27 00:00:00	DKq-UpRSF-1	"""Example"""	null\n''')
    posts_csv.close()
    #add for same date
    eventminer.miner.mine_post("https://www.instagram.com/p/DKq-UpRSF-1/", True)
    posts_csv = open(Posts.POSTS_PATH).readlines()

    # added to postcsv and created image
    assert len(posts_csv) == 3
    assert path.exists(Posts.IMAGE_DIR + "/DKq-UpRSF-1.jpg")

    #clean up
    cleanup()

def test_mine_user():
    eventminer.credentials.load_credentials()
    username = "instagram"
    user_data = eventminer.miner.mine_user(username, {})
    assert user_data["user_id"] == '25025320'

def test_mine_posts_no_id():
    '''User information for users without instagram accounts.'''
    assert path.exists(eventminer.users.USERS_PATH) == False, "Users CSV should not exist before mining."
    
    file = open(eventminer.users.USERS_PATH, "w")
    file.write(",".join(eventminer.users.USERS_KEYS) + "\n" + ",".join(["a", "null", "null", "null", "null"]))
    file.close()
    eventminer.credentials.load_credentials()
    user_data = eventminer.miner.mine_posts()
    assert True
    #clean up
    cleanup()