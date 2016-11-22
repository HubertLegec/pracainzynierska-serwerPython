import logging
from flask_restful import Resource
from flask import request, jsonify
from . import ImageRepository


class HistogramSearcher(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']
        self.api = kwargs['api']
        self.log = logging.getLogger('web.HistogramSearcher')

    def get(self, limit=4):
        """Returns list of urls to images that matches payload, size of list is limited by <limit>"""
        self.log.info('histogram search with limit' + str(limit))
        img_paths = self.search_engine.find_by_histogram(request.data, limit)
        self.log.info('search result size: ' + str(len(img_paths)))
        img_urls = [self.create_url_for_path(path) for path in img_paths]
        return HistogramSearcher.create_json_response(img_urls)

    def create_url_for_path(self, path):
        """Creates url to image with given path"""
        return self.api.url_for(ImageRepository, name=path, _external=True)

    @classmethod
    def create_json_response(cls, urls):
        json = jsonify(images=urls)
        return json
