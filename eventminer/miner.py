from instagrapi import Client
from os import path

from .users import *
from . import credentials

cl = Client()
cl.delay_range = [1, 3]

LOGIN = False

def login():
   global LOGIN
   if LOGIN: return
   '''
   Handle login before any command.
   '''
   cl.set_proxy(('https://user-%s-country-%s:%s@%s' % (credentials.PROXY_USERNAME, credentials.PROXY_COUNTRY, credentials.PROXY_PASSWORD, credentials.PROXY_PROXY)))


   if path.exists(credentials.SESSION_PATH):
      cl.load_settings(credentials.SESSION_PATH)
   cl.login(credentials.INSTAGRAM_USERNAME, credentials.INSTAGRAM_PASSWORD)
   cl.dump_settings(credentials.SESSION_PATH)
   cl.get_timeline_feed()
   LOGIN = True


def mine_user(username, user_data):
   login()

   return

def mine_users(usernames):
   for username in usernames:
      #get user data
      user_data = dict.fromkeys(USERS_KEYS)
      if username in USERS:
         user_data = USERS[username]

      #do we need to update?
      if not user_data["user_id"] or not user_data['full_name']:
         user_data = mine_user(username, user_data)

def update_users():
   usernames = get_usernames()
   users = get_users()
   mine_users(usernames)
   write_users()
   return

def update_posts():
   update_users()
   return 