from eventminer import config

from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import json
import os

import pytest

def now():
    return datetime.now(timezone.utc)


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setattr(config, "CONFIG_PATH", "test_config.json")
    if os.path.exists("test_config.json"):  os.remove("test_config.json")

def test_load_no_conifg(monkeypatch):
    config.__load_config()
    data = json.load(open(config.CONFIG_PATH))
    assert data['start_date'] == "default"
    assert data['last_run'] == None

    os.remove(config.CONFIG_PATH)

def test_load_config(monkeypatch):
    json.dump({
        "start_date": "default",
        "last_run": None
    }, open(config.CONFIG_PATH, "w"))
    config.__load_config()
    assert config.options['start_date'] == "default"
    assert config.options['last_run'] == None
    os.remove(config.CONFIG_PATH)

def test_get_empty_config(monkeypatch):
    options = config.get_config()
    assert config.options['start_date'].date() == (now()+relativedelta(months=-1)).date() #this would fail if there was a day change
    assert config.options['last_run'] == None
    os.remove(config.CONFIG_PATH)

def test_set_first_run_config(monkeypatch):
    options = config.get_config()
    config.set_config()
    assert config.options['start_date'].date() == (now()+relativedelta(months=-1)).date() #this would fail if there was a day change
    assert config.options['last_run'].date() == now().date()
    os.remove(config.CONFIG_PATH)

def test_set_then_load(monkeypatch):
    json.dump({
        "start_date": "2025-06-09",
        "last_run": "2025-06-09"
    }, open(config.CONFIG_PATH, "w"))
    options = config.get_config()
    assert config.options['start_date'] == datetime.fromisoformat("2025-06-09")
    assert config.options['last_run'] == datetime.fromisoformat("2025-06-09")
    os.remove(config.CONFIG_PATH)