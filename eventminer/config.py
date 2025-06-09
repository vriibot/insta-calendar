"""
Handle loading of configuration settings.
"""
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta
import json
from os import path

CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
    # point to start mining posts from when there is no last run
    # will automatically update after first run
    # options: 
    #   "default" - start one month back from current date
    #   null - get all posts
    #   ISO formatted string - set date
    "start_date": "default",
    # automatically updated last run time
    # automatically updates every run
    "last_run": None,
    # for development: ignore the recorded last run
    "ignore_last_run": False,
    # number of posts to download at one time
    "posts_per_page": 50,
}

CURRENT_RUN = datetime.now(timezone.utc)

options = None

def __set_default(options, key):
    if key not in options: options[key] = DEFAULT_CONFIG[key]

def __parse_config():
    global options
    '''
    Internal
    Parses config options.
    '''
    if(options["start_date"] == "default"):
        options["start_date"] = CURRENT_RUN +relativedelta(months=-1)
    elif(options['start_date'] != None):
        options["start_date"] = datetime.fromisoformat(options["start_date"])

    if(options['last_run'] != None):
        options["last_run"] = datetime.fromisoformat(options["last_run"])

    #set defaults
    __set_default(options, "posts_per_page")
    __set_default(options, "ignore_last_run")

def __create_config():
    '''
    Internal
    Create a default config file.
    '''
    file = open(CONFIG_PATH, "w")
    json.dump(DEFAULT_CONFIG, file)
    file.close()

def __load_config():
    global options
    '''
    Internal
    Loads config file but doesn't parse any data.
    '''
    if not path.exists(CONFIG_PATH):
        __create_config()
    options = json.load(open(CONFIG_PATH, "r"))

def get_config():
    global options
    '''
    Loads and returns config options.
    '''
    __load_config()
    __parse_config()
    return options

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def set_config():
    '''
    Write the final version of config.
    '''
    options["last_run"] = CURRENT_RUN
    json.dump(options, open(CONFIG_PATH, "w"), default=json_serial, indent=0)