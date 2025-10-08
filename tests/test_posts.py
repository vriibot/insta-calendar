from eventminer.posts import Posts

import datetime
import os
from os import path
import shutil

currentYear = datetime.datetime.now().year

def cleanup():
    Posts.POSTS = {}
    Posts.EVENT_DATES = []
    Posts.IMAGE_DIR = "testimages"
    Posts.POSTS_PATH = "test_posts.csv"
    if(path.exists(Posts.POSTS_PATH )): os.remove(Posts.POSTS_PATH)
    if(path.exists(Posts.IMAGE_DIR)): shutil.rmtree(Posts.IMAGE_DIR, True)

cleanup()

def test_load_empty_posts():
    assert Posts.POSTS == {}, "Posts should be empty before loading."
    assert Posts.EVENT_DATES == [], "Event dates should be empty before loading."
    Posts.load_posts()
    assert Posts.POSTS == {}, "Posts should remain empty after loading from a non-existent file." 
    assert Posts.EVENT_DATES == [], "Event dates should remain empty after loading from a non-existent file."
    cleanup()

def test_load_posts():
    assert Posts.POSTS == {}, "Posts should be empty before loading."
    assert Posts.EVENT_DATES == [], "Event dates should be empty before loading."
    posts_csv = open(Posts.POSTS_PATH, "w", encoding="utf-8")
    posts_csv.write("\t".join(Posts.POSTS_KEYS) + "\n" + '''00_00	instacalendar_test	2025-06-09T07:21:19+00:00	2025-06-27 00:00:00	DKq-UpRSF-1	"""Example"""	null\t\n''')
    posts_csv.close()
    Posts.load_posts()
    assert Posts.POSTS != {}
    assert Posts.EVENT_DATES != []
    cleanup()

def test_update_posts():
    assert Posts.POSTS == {}, "Posts should be empty before loading."
    assert Posts.EVENT_DATES == [], "Event dates should be empty before loading."
    Posts.load_posts()
    Posts.POSTS = {
        "00_00": {
            "media_id": "00_00",
            "username": "instacalendar_test",
            "post_date": "2025-06-09T07:21:19+00:00",
            "event_date": "2025-06-27 00:00:00",
            "code": "DKq-UpRSF-1",
            "description": '"""Example"""',
            "alt_text": "null",
            "image_url": "null"
        }
    }
    Posts.update_posts()
    assert path.exists(Posts.POSTS_PATH), "Posts CSV file should be created after updating posts."
    cleanup()

def test_parse_date():

    #expected results table
    tests = {
        "1st": None,
        '19:00/19:30': None,
        '21:45-22:15': None,
        "2025.7.1": datetime.datetime(2025, 7, 1),
        '2025.6.13.Fri': datetime.datetime(2025, 6, 13, 0, 0),
        '7/19': datetime.datetime(currentYear, 7, 19, 0, 0),
        '22.HARD': None,
        '2MAN': None,
        '+1drink': None,
        '20250501': None, 
        '7月21日': datetime.datetime(currentYear, 7, 21, 0, 0),
        #27th june
        #june 27th
    }

    for t in tests:
        assert Posts.parse_date(t) == tests[t]

def test_get_date_assumed_before_post():
    date_string = "1/15"
    post_date = datetime.datetime(2025, 6, 1).isoformat()

    # date should be after post date
    assert Posts.get_dates(date_string, post_date) >= datetime.datetime(2026, 1, 15)

def test_date_edge():
    date_string = "9/22"
    post_date = "2025-09-22T02:42:28+00:00"
    assert Posts.get_dates(date_string, post_date) == datetime.datetime(currentYear, 9, 22)