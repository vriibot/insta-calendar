from eventminer import miner
from eventminer import credentials

miner.LOGIN = False

def test_login():
    miner.LOGIN = False
    credentials.load_credentials()
    try:
        miner.login()
    except Exception:
        assert False
    assert miner.LOGIN == True