from eventminer import Users


import json
from os import path
import sys
import pathlib

AUTHOR_PATH = "site/_authors/"

FORCE = False
if len(sys.argv) > 1:
    if sys.argv[1] == "-f":
        FORCE = True

pathlib.Path(AUTHOR_PATH).mkdir(parents=True, exist_ok=True) 

def main():
    users = Users.get_users()
    for user in users:
        user_data = users[user]
        user_path = AUTHOR_PATH + user + ".md"
        if path.exists(user_path) and not FORCE:
            continue
        user_file = open(user_path, "w", encoding="utf-8")
        user_file.write("---\n")
        user_file.write(f"name: \"{user_data['full_name']}\"\n")
        user_file.write(f"short_name: \"{user_data['username']}\"\n")
        user_file.write(f"username: {user_data['username']}\n")
        user_file.write(f"image: {user_data['profile_pic_url']}\n")
        address = user_data['address_street']
        if address:
            address = "\"" + address + "\""
        user_file.write(f"address: {address}\n")
        user_file.write(f"longitude: {user_data['longitude']}\n")
        user_file.write(f"latitude: {user_data['latitude']}\n")
        user_file.write(f"external: {user_data['external']}\n")
        user_file.write(f"external_url: {user_data['external_url']}\n")
        user_file.write("---\n")
        if user_data['biography']:
            biography = json.loads(user_data['biography']).replace("\n", "<br>\n").replace("<br>\n<br>\n", "\n\n")
            user_file.write(biography + "\n")
        user_file.close()

main()