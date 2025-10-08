# handler for cloudinary API

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from eventminer.handler.base import BaseUploadHandler

__all__ = ['CloudinaryHandler']

class CloudinaryHandler(BaseUploadHandler):
    def __init__(self):
        self.CLOUDINARY_CREDENTIALS_PATH = "CLOUDINARY_KEY"
        self.CLOUDINARY_CLOUD_NAME = None
        self.CLOUDINARY_API_KEY = None
        self.CLOUDINARY_API_SECRET = None

        #underlying api object
        self.API = None

    def setup(self):
        #via file
        if 'CLOUDINARY_CLOUD_NAME' in os.environ and 'CLOUDINARY_API_KEY' in os.environ and 'CLOUDINARY_API_SECRET' in os.environ:
            self.CLOUDINARY_CLOUD_NAME = os.environ['CLOUDINARY_CLOUD_NAME']
            self.CLOUDINARY_API_KEY = os.environ['CLOUDINARY_API_KEY']
            self.CLOUDINARY_API_SECRET = os.environ['CLOUDINARY_API_SECRET']
        #via env
        elif os.path.exists(self.CLOUDINARY_CREDENTIALS_PATH):
            file = open(self.CLOUDINARY_CREDENTIALS_PATH)
            lines = file.readlines()
            self.CLOUDINARY_CLOUD_NAME = lines[0].strip()
            self.CLOUDINARY_API_KEY = lines[1].strip()
            self.CLOUDINARY_API_SECRET = lines[2].strip()
        #missing
        else:
            return False
        
        self.API = cloudinary.config(
            cloud_name= self.CLOUDINARY_CLOUD_NAME,
            api_key= self.CLOUDINARY_API_KEY,
            api_secret= self.CLOUDINARY_API_SECRET
        )
        return self.API
    
    def upload(self, path, **kwargs):
        result = cloudinary.uploader.upload(path, use_filename = True, unique_filename = False, overwrite=True)
        return result['secure_url']

    def lookup(self, public_id):
        result = cloudinary.api.resource(public_id)
        return result['secure_url']