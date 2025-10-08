import sys
import os
from os import path
import eventminer
from eventminer.handler import CloudinaryHandler
import pathlib 

def main():
    #handle credentials
    eventminer.load_credentials()

    #load config
    eventminer.get_config()

    #update posts
    eventminer.update_posts(eventminer.Uploader(CloudinaryHandler()))

    #update config
    eventminer.set_config()

main()
