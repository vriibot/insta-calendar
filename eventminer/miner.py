from instagrapi import Client
from os import path
import json

from .users import *
from . import credentials

cl = Client()
cl.delay_range = [1, 3]

LOGIN = False

def login():
   '''
   Handle login before any command.
   '''

   global LOGIN
   if LOGIN: return
   cl.set_proxy(('https://user-%s-country-%s:%s@%s' % (credentials.PROXY['username'], credentials.PROXY['country'], credentials.PROXY['password'], credentials.PROXY['host_port'])))

   session = None
   if path.exists(credentials.SESSION_PATH):
      session = cl.load_settings(credentials.SESSION_PATH)

   if session:
      cl.set_settings(session)
      cl.login(credentials.INSTAGRAM_USERNAME, credentials.INSTAGRAM_PASSWORD)

      try:
            cl.get_timeline_feed()
      except Exception:
         # logger.info("Session is invalid, need to login via username and password")

         old_session = cl.get_settings()

         # use the same device uuids across logins
         cl.set_settings({})
         cl.set_uuids(old_session["uuids"])

         cl.login(credentials.INSTAGRAM_USERNAME, credentials.INSTAGRAM_PASSWORD)
         cl.get_timeline_feed()

      cl.dump_settings(credentials.SESSION_PATH)
   else:
      cl.login(credentials.INSTAGRAM_USERNAME, credentials.INSTAGRAM_PASSWORD)
      cl.get_timeline_feed()
      cl.dump_settings(credentials.SESSION_PATH)
   LOGIN = True


def mine_user(username, user_data):
   login()
   # info = cl.user_info_by_username(username).dict()
   # #is_private
   # #url
   # user_data["user_id"] = info["pk"]
   # user_data["full_name"] = info["full_name"]
   #             # except Exception as e:
   #             #  if isinstance(e, UserNotFound):
   #             #      print(e)
   return

def get_user_media(cl, user):
    posts = []
    user_id = USERS[user]["user_id"]
    medias = cl.user_medias(user_id, 10)
    for m in medias:
        print(m)
        p = process_media(m)
        posts.append(p)
    json.dump(posts, open("data/media_example.json", "w", encoding="utf-8"))

def process_media(m):
    post = {
        'pk': m.pk,
        'id': m.id,
        'code':m.code,
        'taken_at': m.taken_at.timestamp(), #datetime
        'media_type':m.media_type,
        'image_versions2': m.image_versions2,
        # 'product_type': m.product_type,
        # 'thumbnail_url': #httpURL
        # 'location': m.location, #location
        # 'user': {
        #     'pk': m.user.pk,
        #     'username': m.user.username,
        #     'full_name': m.user.fullname,
        #     'profile_pic_url': #httpUrl
        #     'profile_pic_url_hd' :
        #     'is_private': m.user.is_private,
        # },
        'caption_text': m.caption_text,
        'accessibility_caption':m.accessibility_caption,
        # 'user_tags': m.user_tags,
        # 'sponser_tags': m.sponser_tags,
        # 'video_url': m.video_url,
    }
    return post

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