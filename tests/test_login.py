from eventminer import login

def test_passed_credentials():
    login.passed_credentials(["username", "password", "username", "password", "country", "proxy"])
    assert login.INSTAGRAM_USERNAME == "username"
    assert login.INSTAGRAM_PASSWORD == "password"
    assert login.PROXY_USERNAME == "username"
    assert login.PROXY_PASSWORD == "password"
    assert login.PROXY_COUNTRY == "country"
    assert login.PROXY_PROXY == "proxy"