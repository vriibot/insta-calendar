# script to upload all images in site/assets/images/posts/ to cloudinary and overwrite image links in markdown files in site/_posts/

from eventminer.handler import CloudinaryHandler
from eventminer import Uploader
import os

uploader = Uploader(CloudinaryHandler())
uploader.setup()

#upload all images
for file in os.listdir("site/assets/images/posts/"):
    uploader.upload(f"site/assets/images/posts/{file}")
    os.remove(f"site/assets/images/posts/{file}")

#overwrite image links in markdown files
for f  in os.listdir("site/_posts/"):
    file = open(f"site/_posts/{f}", "r", encoding="utf-8")
    content = file.readlines()
    file.close()

    #find line starting with image
    for i, line in enumerate(content):
        if line.startswith("image: "):
            path = line.split("/")[-1].split(".")[0]
            url = uploader.lookup(path)
            line = "image: " + url + "\n"
            content[i] = line   
            content = "".join(content)
            file = open(f"site/_posts/{f}", "w", encoding="utf-8")
            file.write(content)
            file.close()
            break
    