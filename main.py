import sys
import os
from os import path
import eventminer
import pathlib 

def main():
    #handle credentials
    eventminer.load_credentials()

    #load config
    eventminer.get_config()

    #setup asset folder
    if not path.exists(eventminer.IMAGE_DIR): pathlib.Path(eventminer.IMAGE_DIR).mkdir(parents=True, exist_ok=True) 

    #update posts
    eventminer.update_posts()

    #update config
    eventminer.set_config()

main()
