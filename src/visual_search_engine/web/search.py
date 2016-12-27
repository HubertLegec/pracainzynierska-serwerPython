import logging
from flask import request
from . import BaseSearcher


class Searcher(BaseSearcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = logging.getLogger('vse.Searcher')

    def post(self, limit=4):
        """Returns list of urls to images that matches payload, size of list is limited by <limit>"""
        self.log.info('image search with limit: ' + str(limit))
        query_file = request.files['image'].read()
        result = self.search_engine.find(query_file, limit)
        self.log.info('search result size: ' + str(len(result)))
        img_descriptions = self.create_images_descriptions(result)
        return self.create_json_response(img_descriptions)



