"""
Handles the reading and writing of post data files and their objects.
"""
import csv
from os import path
import os
import json
import dateparser
import datetime
from dateparser_data.settings import default_parsers
parsers = [parser for parser in default_parsers if parser != 'relative-time']
languages = ['en', 'ja']

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

POSTS_PATH = "data/posts.csv"
POSTS_KEYS = ["media_id", "username", 'post_date', 'event_date', "code", 'description', 'alt_text']
IMAGE_DIR = "site/assets/images/posts"

# map of id to post data
POSTS = {}
EVENT_DATES=[]

def get_posts():
    '''
    Load posts from CSV.
    '''
    global POSTS
    #always reset when re-reading from csv
    POSTS = {}
    if not path.exists(POSTS_PATH): return POSTS
    with open(POSTS_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            POSTS[row["media_id"]] = row
    for p in POSTS:
        p = POSTS[p]
        EVENT_DATES.append(p['event_date']+p['username'])
    return POSTS

def write_posts():
    '''
    Update posts CSV.
    '''
    global POSTS
    with open(POSTS_PATH, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, POSTS_KEYS, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for media in POSTS.keys():
            writer.writerow(POSTS[media])

def __parse_date(string, date_order = None):
     '''
     Internal function to handle dateparser and its settings.
     Date order can be provided.
     Assuming order issues will come up at some point. Should probably be set per user.
     Strings given may not always be dates. Additional filtering can be done prior.
     Number only strings are not handled because of false positives.
     I suppose if someone uses them it again has to be set per user.
     '''
     settings = {"REQUIRE_PARTS": ['day', 'month'], 'PARSERS': parsers, 'DEFAULT_LANGUAGES': languages}
     if date_order: settings['DATE_ORDER'] = date_order
     return dateparser.parse(string, settings=settings)

def get_dates(description):
    dates = []
    # print(description)
    lines = description.split("\n")
    for line in lines:
        line = line.split(" ")[0]
        line = line.split("(")[0]
        if has_numbers(line):
            # dates.append([line, __parse_date(line)])
            date = __parse_date(line)
            # print([date, line])
            if date:
                dates.append(date)
    if len(dates) != 1: return None
    return dates[0]

def get_first_image(p):
    url = None
    resources = p['resources']
    if len(resources) < 1: 
        return p["image_versions2"]['candidates'][0]['url']
    for r in p["resources"]:
        if r['media_type'] == 1:
            return r['thumbnail_url']
    return None

def filter_posts(posts, force_same_day = False):
    filtered_posts = []
    for p in posts:
        if p["media_type"] != 1 and p["media_type"] != 8: continue # is not image or collection
        p['first_image'] = get_first_image(p)
        if(p['first_image'] == None): continue #collection of all videos
        p['event_date'] = get_dates(p['description'])
        if not p['event_date']: continue

        filtered_posts.append(p)

    #if new date, add
    if not force_same_day:
        posts = filtered_posts
        filtered_posts = []
        for p in posts[::-1]:
            date = p['event_date']
            if str(date)+p['username'] in EVENT_DATES: continue
            EVENT_DATES.append(str(date)+p['username'] )
            filtered_posts.append(p)

    return filtered_posts