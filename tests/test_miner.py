from eventminer import miner
from eventminer import credentials
import os

miner.LOGIN = False


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
    credentials.load_credentials()
    miner.LOGIN = False
    # try:
    miner.login()
    # except Exception:
    #     assert False
    assert miner.LOGIN == True

def test_mine_bad_user():
    username = "a"
    user_data = miner.mine_user(username, {})
    assert len(list(user_data.keys())) == 0

# def test_mine_user():
#     credentials.load_credentials()
#     username = "instagram"
#     user_data = miner.mine_user(username, {})
#     assert user_data["user_id"] == '25025320'