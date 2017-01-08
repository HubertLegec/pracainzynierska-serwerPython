import logging
from flask_restful import Resource


class ImageRepository(Resource):

    def __init__(self, **kwargs):
        self.log = logging.getLogger('vse.ImageRepository')
        self.search_engine = kwargs['search_engine']

    def get(self, file):
        self.log.info('Get image request for: ' + file)
        return self.search_engine.repository.get(file)
