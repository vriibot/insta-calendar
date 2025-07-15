import eventminer
import os
from os import path
import pytest
import shutil

eventminer.miner.LOGIN = False
eventminer.posts.IMAGE_DIR = "testimages"
eventminer.posts.POSTS_PATH = "test_posts.csv"
eventminer.users.USERS_PATH = "test_users.csv"
if(path.exists(eventminer.users.USERNAMES_PATH)): os.remove(eventminer.users.USERNAMES_PATH)
if(path.exists(eventminer.posts.POSTS_PATH )): os.remove(eventminer.posts.POSTS_PATH)
if(path.exists(eventminer.posts.IMAGE_DIR)): shutil.rmtree(eventminer.posts.IMAGE_DIR, True)


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
    eventminer.credentials.load_credentials()
    eventminer.credentials.LOGIN = False
    # try:
    eventminer.miner.login()
    # except Exception:
    #     assert False
    assert eventminer.miner.LOGIN == True

def test_mine_bad_user():
    username = "a"
    user_data = eventminer.miner.mine_user(username, {})
    assert len(list(user_data.keys())) == 0

def test_mine_post():
    eventminer.credentials.load_credentials()
    eventminer.miner.login()
    eventminer.miner.mine_post("https://www.instagram.com/p/DKq-UpRSF-1/")
    posts_csv = open(eventminer.posts.POSTS_PATH).readlines()

    # added to postcsv and created image
    assert len(posts_csv) == 2
    assert path.exists(eventminer.posts.IMAGE_DIR + "/DKq-UpRSF-1.jpg")

    #clean up
    if(path.exists(eventminer.posts.IMAGE_DIR)): shutil.rmtree(eventminer.posts.IMAGE_DIR, True)
    if(path.exists(eventminer.posts.POSTS_PATH )): os.remove(eventminer.posts.POSTS_PATH)

def test_mine_post_force_same_date():
    eventminer.credentials.load_credentials()
    eventminer.miner.login()

    #setup existing event
    posts_csv = open(eventminer.posts.POSTS_PATH, "w")
    posts_csv.write("\t".join(eventminer.posts.POSTS_KEYS) + "\n" + '''00_00	instacalendar_test	2025-06-09T07:21:19+00:00	2025-06-27 00:00:00	DKq-UpRSF-1	"""Example"""	null\n''')
    posts_csv.close()
    #add for same date
    eventminer.miner.mine_post("https://www.instagram.com/p/DKq-UpRSF-1/", True)
    posts_csv = open(eventminer.posts.POSTS_PATH).readlines()

    # added to postcsv and created image
    assert len(posts_csv) == 3
    assert path.exists(eventminer.posts.IMAGE_DIR + "/DKq-UpRSF-1.jpg")

    #clean up
    if(path.exists(eventminer.posts.IMAGE_DIR)): shutil.rmtree(eventminer.posts.IMAGE_DIR, True)
    if(path.exists(eventminer.posts.POSTS_PATH )): os.remove(eventminer.posts.POSTS_PATH)

def test_mine_user():
    eventminer.credentials.load_credentials()
    username = "instagram"
    user_data = eventminer.miner.mine_user(username, {})
    assert user_data["user_id"] == '25025320'

def test_mine_posts_no_id():
    '''User information for users without instagram accounts.'''
    file = open(eventminer.users.USERS_PATH, "w")
    file.write(",".join(eventminer.users.USERS_KEYS) + "\n" + ",".join(["a", "null", "null", "null", "null"]))
    file.close()
    eventminer.credentials.load_credentials()
    user_data = eventminer.miner.mine_posts()
    assert True
    #clean up
    if(path.exists(eventminer.users.USERS_PATH)): os.remove(eventminer.users.USERS_PATH)