from os import path
import pathlib 
import sys

import eventminer

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
    #mine post
    eventminer.mine_post(url, FORCE)

main()