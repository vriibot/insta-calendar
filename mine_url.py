from os import path
import pathlib 
import sys

import eventminer

def main():
    args = sys.argv[1:]
    url = None
    if(len(args) >= 1):
        url = args[0]
    
    #handle credentials
    eventminer.load_credentials()
    if not path.exists(eventminer.IMAGE_DIR): pathlib.Path(eventminer.IMAGE_DIR).mkdir(parents=True, exist_ok=True) 
    #mine post
    eventminer.mine_post(url)

main()