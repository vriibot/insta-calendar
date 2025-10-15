from os import path
import pathlib 
import sys

import eventminer
from eventminer.uploader import Uploader
from eventminer.handler.cloudinary import CloudinaryHandler

uploader = Uploader(CloudinaryHandler())
uploader.setup()

FORCE = False

def main():
    global FORCE
    args = sys.argv[1:]
    url = None
    if "-f" in args:
        FORCE = True
    if(len(args) >= 1):
        url = args[0]
    
    #handle credentials
    eventminer.load_credentials()

    eventminer.miner.UPLOADER = uploader
    #mine post
    eventminer.mine_post(url, FORCE)

main()