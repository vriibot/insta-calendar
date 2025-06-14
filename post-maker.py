import csv
from os import path
from datetime import datetime
import json
import pathlib
from string import punctuation

TAGS_PATH = "tags.txt"
POSTS_PATH = "data/posts.csv"
POSTS_DIR = "site/_posts/"
POSTS_KEYS = ["media_id", "username", 'post_date', "code", 'description', 'alt_text', 'event_date']
IMAGES_DIR = "assets/images/"

def has_alpha(inputString):
    return any(char.isalpha() for char in inputString)

pathlib.Path(POSTS_DIR).mkdir(parents=True, exist_ok=True) 

TAG_IGNORE = []
TAG_INCLUDE = []
TAG_MATCHES = []

def process_tag_list():
    if not path.exists(TAGS_PATH): return
    file = open(TAGS_PATH, "r")
    for line in file.readlines():
        line=line.strip()
        if line.startswith("-"):
            TAG_IGNORE.append(line[1:].lower())
        elif line.startswith("*"):
            TAG_MATCHES.append(line[1:])
        else: TAG_INCLUDE.append(line.lower())

def extract_tags(description):
    tags = []
    words = description.split()
    for word in words:
        word = word.lower()
        if word.startswith("#") and word[1:] not in TAG_IGNORE: 
            tags.append(word[1:])
        if word.strip(punctuation) in TAG_INCLUDE:
            tags.append(word.strip(punctuation))

    for t in TAG_MATCHES:
        if t in description: 
            tags.append(t)
    return tags

def extract_title(description):
    title = ""
    for line in description.split("\n"):
        if not line.strip(punctuation): continue
        if not has_alpha(line): continue
        elif not title: title = line
    return title


def main():
    if not path.exists(POSTS_PATH): return
    process_tag_list()
    with open(POSTS_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            date_string = str(datetime.fromisoformat(row["event_date"]).date())
            file_name = date_string + "-" + row['media_id'].replace("_", "-") + ".md"
            # if(path.exists(POSTS_DIR + file_name)): continue
            description = json.loads(row["description"])
            title = extract_title(description)
            tags = extract_tags(description)
            tags = "- " + "\n- ".join(tags)
            file = open(POSTS_DIR + file_name, "w")
            file.write("---\nauthor: "+ row["username"]+ "\nimage: " + IMAGES_DIR + row["code"] + ".jpg\n" + "title: "+title+"\ndate: " + date_string + "\nsource: 'https:/instagram.com/p/" + row["code"] +"'\ntags:\n" + tags + "\n---\n" + description)
            file.close()

main()