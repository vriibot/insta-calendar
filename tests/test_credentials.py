from eventminer import credentials
import os
from os import path
import pytest

default_proxy = dict(credentials.PROXY)

def clear_env(monkeypatch, vars):
    for v in vars:
        if v in os.environ:
            monkeypatch.delenv(v)

def set_env(monkeypatch, vars, values):
    i=-1
    for v in vars:
        i+=1
        monkeypatch.setenv(v, values[i])

@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setattr(credentials, "PROXY_PATH", "test_proxy")
    monkeypatch.setattr(credentials, "INSTAGRAM_CREDENTIALS_PATH", "test_credentials")


def test_load_local_credentials(monkeypatch):
    #remove these two env vars to trigger load from file
    clear_env(monkeypatch, ["INSTAGRAM_USERNAME", "PROXY_USERNAME"])
    file = open(credentials.PROXY_PATH, "w")
    file.write("username\npassword\ncountry\nhost:0000")
    file.close()
    file = open(credentials.INSTAGRAM_CREDENTIALS_PATH, "w")
    file.write("username\npassword\n")
    file.close()
    credentials.load_credentials()
    assert credentials.INSTAGRAM_USERNAME == "username"
    assert credentials.INSTAGRAM_PASSWORD == "password"
    assert credentials.PROXY["username"] == "username"
    assert credentials.PROXY["password"]  == "password"
    assert credentials.PROXY["country"]  == "country"
    assert credentials.PROXY["host_port"]  == "host:0000"
    os.remove(credentials.PROXY_PATH)
    os.remove(credentials.INSTAGRAM_CREDENTIALS_PATH)
    monkeypatch.undo()
    credentials.load_credentials()

def test_load_env_credentials(monkeypatch):
    #set all env vars
    set_env(monkeypatch, ["INSTAGRAM_USERNAME", "INSTAGRAM_PASSWORD", "PROXY_USERNAME", "PROXY_PASSWORD", "PROXY_COUNTRY", "PROXY_HOST_PORT"], ["username", "password", "username", "password", "country", "host:1000"])
    credentials.load_credentials()
    assert credentials.INSTAGRAM_USERNAME == "username"
    assert credentials.INSTAGRAM_PASSWORD == "password"
    assert credentials.PROXY["username"] == "username"
    assert credentials.PROXY["password"]  == "password"
    assert credentials.PROXY["country"]  == "country"
    assert credentials.PROXY["host_port"]  == "host:1000"

    monkeypatch.undo()
    credentials.load_credentials()