"""
Handles loading of credentials.
"""

import os

INSTAGRAM_CREDENTIALS_PATH = "INSTAGRAM_KEY"
PROXY_PATH = "PROXY_KEY"
SESSION_PATH = "data/session.json"

if(not os.path.exists("data")): os.mkdir("data")

INSTAGRAM_USERNAME = None
INSTAGRAM_PASSWORD = None

PROXY = {
    "username":None,
    "country":None,
    "password":None,
    "host_port": None
}


def load_credentials():
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, PROXY
    if "INSTAGRAM_USERNAME" in os.environ and "INSTAGRAM_PASSWORD" in os.environ: 
        INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USERNAME"]
        INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]
    else:
        file = open(INSTAGRAM_CREDENTIALS_PATH)
        lines = file.readlines()
        INSTAGRAM_USERNAME = lines[0].strip()
        INSTAGRAM_PASSWORD = lines[1].strip()

    if "PROXY_USERNAME" in os.environ and "PROXY_PASSWORD" in os.environ and "PROXY_COUNTRY" in os.environ and "PROXY_HOST_PORT" in os.environ:
            PROXY['username'] =  os.environ["PROXY_USERNAME"]
            PROXY['password']= os.environ["PROXY_PASSWORD"]
            PROXY['country'] = os.environ["PROXY_COUNTRY"]
            PROXY['host_port'] = os.environ["PROXY_HOST_PORT"]
    else:
        file = open(PROXY_PATH)
        lines = file.readlines()
        PROXY['username'] = lines[0].strip()
        PROXY['password']= lines[1].strip()
        PROXY['country'] = lines[2].strip()
        PROXY['host_port'] = lines[3].strip()