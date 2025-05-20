INSTAGRAM_CREDENTIALS_PATH = "INSTAGRAM_KEY"

INSTAGRAM_USERNAME = None
INSTAGRAM_PASSWORD = None

PROXY_USERNAME = None
PROXY_PASSWORD = None
PROXY_COUNTRY = None
PROXY_PROXY = None


def local_credentials():
    '''
    Load credentials from local files.
    '''
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD
    file = open(INSTAGRAM_CREDENTIALS_PATH)
    lines = file.readlines()
    INSTAGRAM_USERNAME = lines[0].strip()
    INSTAGRAM_PASSWORD = lines[1].strip()
    return

def passed_credentials(args):
    '''
    Load credentials from arguments, for use with GitHub secrets.
    '''
    global INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, PROXY_USERNAME, PROXY_PASSWORD, PROXY_COUNTRY, PROXY_PROXY
    INSTAGRAM_USERNAME = args[0].strip()
    INSTAGRAM_PASSWORD = args[1].strip()
    PROXY_USERNAME = args[2].strip()
    PROXY_PASSWORD = args[3].strip()
    PROXY_COUNTRY = args[4].strip()
    PROXY_PROXY = args[5].strip()
    return