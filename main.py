import sys
import eventminer

def main():
    #handle credentials
    eventminer.load_credentials()
    
    # args = sys.argv[1:]
    # if len(args) < 1:
    #     eventminer.local_credentials()
    # else:
    #     eventminer.passed_credentials(args)

    #update posts
    eventminer.update_posts()

main()
