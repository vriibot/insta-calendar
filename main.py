import sys
import os
from os import path
import eventminer

def main():
    #handle credentials
    eventminer.load_credentials()

    #load config
    eventminer.get_config()

    #setup asset folder
    if not path.exists(eventminer.IMAGE_DIR): os.mkdir(eventminer.IMAGE_DIR)

    #update posts
    eventminer.update_posts()

    #update config
    eventminer.set_config()

main()
