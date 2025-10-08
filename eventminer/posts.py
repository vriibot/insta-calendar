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

from eventminer.uploader import Uploader
import eventminer.handler

__all__ = ['Posts']

def has_numbers(inputString):
    '''Check if a string has numbers.'''
    return any(char.isdigit() for char in inputString)

class Posts:
    POSTS_PATH = "data/posts.csv"
    IMAGE_DIR = "site/assets/images/posts"
    POSTS_KEYS = ["media_id", "username", 'post_date', 'event_date', "code", 'description', 'alt_text', 'image_url']
    POSTS = {}
    EVENT_DATES = []
    PARSERS = [parser for parser in default_parsers if parser != 'relative-time']
    LANGUAGES = ['en', 'ja']
    

    @staticmethod
    def load_posts():
        '''
        Load posts from CSV.
        '''
        #always reset when re-reading from csv
        Posts.POSTS = {}
        if not path.exists(Posts.POSTS_PATH): return Posts.POSTS
        with open(Posts.POSTS_PATH, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                Posts.POSTS[row["media_id"]] = row
        for p in Posts.POSTS:
            p = Posts.POSTS[p]
            Posts.EVENT_DATES.append(p['event_date']+p['username'])
        return Posts.POSTS
   
    @staticmethod
    def update_posts():
        '''
        Update posts CSV.
        '''
        with open(Posts.POSTS_PATH, 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, Posts.POSTS_KEYS, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for media in Posts.POSTS.keys():
                writer.writerow(Posts.POSTS[media])
    
    @staticmethod
    def parse_date(string, date_order = None, prefer_future = False):
     '''
     Internal function to handle dateparser and its settings.
     Date order can be provided.
     Assuming order issues will come up at some point. Should probably be set per user.
     Strings given may not always be dates. Additional filtering can be done prior.
     Number only strings are not handled because of false positives.
     I suppose if someone uses them it again has to be set per user.
     '''
     settings = {"REQUIRE_PARTS": ['day', 'month'], 'PARSERS': Posts.PARSERS, 'DEFAULT_LANGUAGES': Posts.LANGUAGES}
     if date_order: settings['DATE_ORDER'] = date_order
     #only set explicitly if needed
     if prefer_future: settings['PREFER_DATES_FROM'] = 'future'
     return dateparser.parse(string, settings=settings)

    @staticmethod
    def get_dates(description, post_date):
        dates = []
        date_lines = []
        # print(description)
        lines = description.split("\n")
        for line in lines:
            line = line.split(" ")[0]
            line = line.split("(")[0]
            if has_numbers(line):
                # dates.append([line, __parse_date(line)])
                date = Posts.parse_date(line)
                # print([date, line])
                if date:
                    dates.append(date)
                    date_lines.append(line)
        if len(dates) != 1: return None
        date = dates[0]
        #guessed dates assume this year but could be next year
        #the best way to check this is that post date should be before event date
        if date.date() < datetime.datetime.fromisoformat(post_date).replace(tzinfo=None).date():
            #redo with prefer future
            date = Posts.parse_date(date_lines[0], prefer_future=True)

        return date
    
    @staticmethod
    def get_first_image(p):
        url = None
        resources = p['resources']
        if len(resources) < 1: 
            return p["image_versions2"]['candidates'][0]['url']
        for r in p["resources"]:
            if r['media_type'] == 1:
                return r['thumbnail_url']
        return None

    @staticmethod
    def filter_posts(posts, force_same_day = False):
        filtered_posts = []
        for p in posts:
            if p["media_type"] != 1 and p["media_type"] != 8: continue # is not image or collection
            p['first_image'] = Posts.get_first_image(p)
            if(p['first_image'] == None): continue #collection of all videos
            p['event_date'] = Posts.get_dates(p['description'], p['post_date'])
            if not p['event_date']: continue

            filtered_posts.append(p)

        #if new date, add
        if not force_same_day:
            posts = filtered_posts
            filtered_posts = []
            for p in posts[::-1]:
                date = p['event_date']
                if str(date)+p['username'] in Posts.EVENT_DATES: continue
                Posts.EVENT_DATES.append(str(date)+p['username'] )
                filtered_posts.append(p)

        return filtered_posts
