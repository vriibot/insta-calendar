from eventminer.handler.base import BaseUploadHandler

__all__ = ['Uploader']

class Uploader:

    def __init__(self, handler: BaseUploadHandler):
        self.handler = handler

    def setup(self):
        return self.handler.setup()

    def upload(self, path):
        return self.handler.upload(path)
    
    def lookup(self, public_id):
        '''Return the URL of an uploaded image given its public ID (filename).'''
        return self.handler.lookup(public_id)