"""
Handles the reading and writing of user data files and their objects.
"""
import csv
import json
from os import path

USERS_PATH = "data/users.csv"
USERNAMES_PATH = "usernames.txt"

USERS_KEYS = ["username", "user_id", "full_name", "is_private", "profile_pic_url", "timestamp"]
# map of usernames to instagram user data
USERS = {}

def get_usernames():
    usernames = []
    file = open(USERNAMES_PATH, "r", encoding="utf-8")
    for line in file.readlines():
        name = line.strip()
        usernames.append(name)
    return usernames

def get_users():
    '''
    Load users object from CSV.
    Return an empty object if file doesn't exist
    Or file is empty.
    '''
    global USERS
    if not path.exists(USERS_PATH): return USERS
    with open(USERS_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["is_private"] = json.loads(row["is_private"].lower())
            USERS[row["username"]] = row
    return USERS

def write_users():
    '''
    Write user data to the user csv.
    '''
    global USERS
    with open(USERS_PATH, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, USERS_KEYS)
        writer.writeheader()
        for user in USERS.keys():
            writer.writerow(USERS[user])
        