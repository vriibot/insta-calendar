"""
Handles the reading and writing of user data files and their objects.
"""
import csv
import json
from os import path

__all__ = ['Users']

class Users:
    USERS_PATH = "data/users.csv"
    USERNAMES_PATH = "usernames.txt"
    USERS_KEYS = ["username", "user_id", "full_name", "is_private", "profile_pic_url", "timestamp", "biography", "address_street", "longitude", "latitude", "external", "external_url"]
    # map of usernames to instagram user data
    USERS = {}
    IMAGE_DIR = "site/assets/images/authors"

    @staticmethod
    def get_usernames():
        '''Return a list of usernames to mine from the user specified usernames file.'''
        usernames = []
        file = open(Users.USERNAMES_PATH, "r", encoding="utf-8")
        for line in file.readlines():
            name = line.strip()
            usernames.append(name)
        return usernames

    @staticmethod
    def get_users():
        '''
        Load users object from CSV.
        Return an empty object if file doesn't exist
        Or file is empty.
        '''
        if not path.exists(Users.USERS_PATH): return Users.USERS
        with open(Users.USERS_PATH, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if(row["is_private"].lower() == "true"): row["is_private"] = True
                else:
                    row["is_private"] = False
                Users.USERS[row["username"]] = row
        return Users.USERS
    
    @staticmethod
    def write_users():
        '''
        Write user data to the user csv.
        '''
        with open(Users.USERS_PATH, 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, Users.USERS_KEYS)
            writer.writeheader()
            for user in Users.USERS.keys():
                writer.writerow(Users.USERS[user])
        