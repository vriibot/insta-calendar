from instagrapi import Client
from instagrapi.exceptions import UserNotFound
from PIL import Image
from pillow_heif import register_heif_opener

import os
from os import path
import json
import pathlib

register_heif_opener()

from .users import *
from . import posts
from . import config
from . import credentials

cl = Client()
cl.delay_range = [1, 5]

LOGIN = False

def login():
   '''
   Handle login before any command.
   '''
   global LOGIN
   if LOGIN: return
   #cl.set_proxy(('https://user-%s-country-%s:%s@%s' % (credentials.PROXY['username'], credentials.PROXY['country'], credentials.PROXY['password'], credentials.PROXY['host_port'])))

   session = None
   if path.exists(credentials.SESSION_PATH):
      session = cl.load_settings(credentials.SESSION_PATH)

   if session:
      cl.set_settings(session)
      cl.login(credentials.INSTAGRAM_USERNAME, credentials.INSTAGRAM_PASSWORD)

      try:
            cl.get_timeline_feed()
      except Exception as e:
         print("session fail", e)
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

def process_media(m):
    '''
    Convert to JSON.
    '''
    post = {
        'media_id': m.id, #includes user id
        'username': m.user.username,
        'code':m.code,
        'post_date': m.taken_at.isoformat(), #datetime
        'media_type':m.media_type,
        'image_versions2': m.image_versions2,
        # 'product_type': m.product_type,
        # 'thumbnail_url': #httpURL
        # 'location': m.location, #location
        # 'user': {
        #     'pk': m.user.pk,
        #     'username': m.user.username,
        #     'full_name': m.user.full_name,
        #     'profile_pic_url': #httpUrl
        #     'profile_pic_url_hd' :
        #     'is_private': m.user.is_private,
        # },
        'description': m.caption_text,
        'alt_text':m.accessibility_caption,
      #   'user_tags': m.user_tags,
        # 'sponser_tags': m.sponser_tags,
        # 'video_url': m.video_url,
        'resources': []
    }
    for r in m.resources:
       post['resources'].append({
          'media_type': r.media_type,
          'thumbnail_url':  str(r.thumbnail_url)
       })
    return post

def get_user_media(user):
   login()
   posts = []
   user_id = USERS[user]["user_id"]

   #get end point
   end = None
   if config.options['last_run']: end = config.options['last_run']
   if config.options['ignore_last_run']: end= None
   if end==None and config.options['start_date']: end = config.options['start_date']

   finished = False
   cursor = None
   page = 0
   while(not finished):
      page += 1
      print("page", page, len(posts))
      # print("run loop", cursor, end, config.options["posts_per_page"])
      medias, cursor = cl.user_medias_paginated(user_id, config.options["posts_per_page"], cursor)

      for i, m in enumerate(medias):
         if end and m.taken_at <= end:
            if page == 1 and i < 3: #ignore pinned
               continue
            finished=True
            break
         p = process_media(m)
         posts.append(p)
      if cursor == "": 
         finished = True
         break
   # json.dump(posts, open("data/media_example"+user+".json", "w", encoding="utf-8"))
   return posts


def mine_user(username, user_data):
   login()

   try:
      info = cl.user_info_by_username(username).dict()
   except UserNotFound as e:
      print(e.message, username)
      return user_data
      
   user_data["user_id"] = info["pk"]
   user_data["full_name"] = info["full_name"]
   user_data["is_private"] = info["is_private"]
   user_data["profile_pic_url"] = str(info["profile_pic_url"])
   return user_data

def mine_users(usernames):
   for username in usernames:
      #get user data
      user_data = dict.fromkeys(USERS_KEYS)
      if username in USERS:
         user_data = USERS[username]
      
      user_data['username'] = username

      #do we need to update?
      if not user_data["user_id"] or not user_data['full_name']:
         user_data = mine_user(username, user_data)
         USERS[username] = user_data

def update_users():
   usernames = get_usernames()
   users = get_users()
   mine_users(usernames)
   write_users()
   return


def convert_to_jpg(input_file, output_file):
    try:
        img = Image.open(input_file)
        img = img.convert("RGB")
        img.save(output_file, "JPEG", quality=95)
        
        # Delete the original .heic file after successful conversion
        os.remove(input_file)
    except Exception as e:
        print(f"Error converting {input_file} to {output_file}: {e}")

def download_photo(url, name, file_path):
   login()
   #check if destination path exists and if not create
   if not path.exists(posts.IMAGE_DIR): 
      pathlib.Path(posts.IMAGE_DIR).mkdir(parents=True, exist_ok=True) 
   #download and get path
   file_path = str(cl.photo_download_by_url(url, name, file_path))
   #convert to jpg
   if(file_path.endswith(".heic")):
      new_path = file_path.replace(".heic", ".jpg")
      convert_to_jpg(file_path, new_path)

def mine_posts():
   posts.get_posts()
   postss = []
   for user in USERS:
      if USERS[user]["is_private"] == False and USERS[user]['user_id'] != 'null':
         # posts += json.load(open("data/media_example"+user+".json", "r", encoding="utf-8"))
         postss += get_user_media(user)
   filtered_posts = posts.filter_posts(postss)
   for p in filtered_posts:
      if p['media_id'] in posts.POSTS: 
         continue
      download_photo(p['first_image'], p['code'], posts.IMAGE_DIR)
      posts.POSTS[p["media_id"]] = {
         "media_id" : p['media_id'],
         "username" : p["username"],
         "post_date" : p['post_date'],
         "code" : p['code'],
         'description': json.dumps(p['description']),
         'alt_text': json.dumps(p['alt_text']),
         'event_date': p['event_date'],
         # 'image_url': p['first_image'] #temporary link
      } 
   # print(POSTS.keys())
   
def mine_post(url, force_same_day=False):
   '''For downloading a specific post by URL.'''
   login()
   posts.get_posts()
   pk = cl.media_pk_from_url(url)
   media = cl.media_info(pk)
   post = process_media(media)
   filtered = posts.filter_posts([post],  force_same_day)
   if(len(filtered) > 0):
      p = filtered[0]
      download_photo(p['first_image'], p['code'], posts.IMAGE_DIR)
      posts.POSTS[p["media_id"]] = {
         "media_id" : p['media_id'],
         "username" : p["username"],
         "post_date" : p['post_date'],
         "code" : p['code'],
         'description': json.dumps(p['description']),
         'alt_text': json.dumps(p['alt_text']),
         'event_date': p['event_date'],
         # 'image_url': p['first_image'] #temporary link
      } 
      posts.write_posts()
   else:
      print(json.dumps(post, indent=2, default=str))


def update_posts():
   update_users()
   mine_posts()
   posts.write_posts()
   return 