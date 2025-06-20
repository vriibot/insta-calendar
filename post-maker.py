import csv
from os import path
from datetime import datetime
import json
import pathlib
from string import punctuation

import demoji

from eventminer import get_users, POSTS_KEYS
from filter import filter

TAGS_PATH = "tags.txt"
POSTS_PATH = "data/posts.csv"
POSTS_DIR = "site/_posts/"

IMAGES_DIR = "assets/images/posts/"

USERS = get_users()

def has_alpha(inputString):
    return any(char.isalpha() for char in inputString)

pathlib.Path(POSTS_DIR).mkdir(parents=True, exist_ok=True) 

TAG_IGNORE = []
TAG_INCLUDE = []
TAG_MATCHES = []

def process_tag_list():
    if not path.exists(TAGS_PATH): return
    file = open(TAGS_PATH, "r", encoding="utf-8")
    for line in file.readlines():
        line=line.strip()
        if line.startswith("-"):
            TAG_IGNORE.append(line[1:].lower())
        elif line.startswith("*"):
            TAG_MATCHES.append(line[1:])
        else: TAG_INCLUDE.append(line.lower())

def extract_tags(description):
    tags = []
    words = demoji.replace(description, " ").split()
    for word in words:
        word = word.lower()
        if word.startswith("#") and word[1:] not in TAG_IGNORE: 
            if(has_alpha(word)):
                tags.append(word[1:])
        if word.strip(punctuation) in TAG_INCLUDE:
            tags.append(word.strip(punctuation).lower())
        elif word in TAG_INCLUDE:
            tags.append(word.lower())

    for t in TAG_MATCHES:
        if t in description: 
            tags.append(t.lower())
    return tags

def extract_title(description):
    title = filter(description)
    if not title: 
        title = ""
        first_line = ""
        for line in description.split("\n"):
            if not line.strip(punctuation).strip(): continue
            if not has_alpha(line): continue
            if '月' in line or '日' in line: continue
            actual_line = []
            for word in line.split():
                if word.startswith("#") or word.startswith("@"): continue
                if not demoji.replace(word.strip(punctuation), ""): continue
                actual_line.append(word)
            if not title and len(actual_line) > 0: 
                title = " ".join(actual_line)
        if not title: tile = first_line
    return '"' + title.replace('"', "'") + '"'


def main():
    if not path.exists(POSTS_PATH): return
    process_tag_list()
    with open(POSTS_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            date_string = str(datetime.fromisoformat(row["event_date"]).date())
            file_name = date_string + "-" + row['media_id'].replace("_", "-") + ".md"
            if(path.exists(POSTS_DIR + file_name)): continue
            name = USERS[row['username']]["full_name"]
            description = json.loads(row["description"])
            title = extract_title(description)
            tags = extract_tags(description)
            tags = "- " + "\n- ".join(tags)
            description = description.replace("\n", "<br>\n").replace("<br>\n<br>\n", "\n\n")
            image_dir = "/" + IMAGES_DIR + row["code"] + ".jpg"
            file = open(POSTS_DIR + file_name, "w", encoding="utf-8")
            file.write("---\nauthor: "+ name + "\nimage: " + image_dir + "\ntitle: "+title+"\ndate: " + date_string + "\nsource: 'https://instagram.com/p/" + row["code"] +"'\ntags:\n" + tags + "\n---\n" + description)
            file.close()

main()