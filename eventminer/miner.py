from .users import *

def update_users():
   usernames = get_usernames()
   users = get_users()
   #mine
   write_users()
   return

def update_posts():
   update_users()
   return 