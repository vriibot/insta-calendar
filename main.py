import sys
import eventminer

def main():
    #handle credentials
    eventminer.load_credentials()

    #update posts
    eventminer.update_posts()

main()
