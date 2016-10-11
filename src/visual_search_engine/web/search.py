import logging
from flask_restful import Resource
from flask import request, make_response, jsonify
from . import ImageRepository


class Searcher(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']
        self.api = kwargs['api']
        self.log = logging.getLogger('Searcher')

    def get(self, limit=4):
        """Returns list of urls to images that matches payload, size of list is limited by <limit>"""
        img_paths = self.search_engine.find(request.data, limit)
        img_urls = [self.create_url_for_path(path) for path in img_paths]
        return Searcher.create_json_response(img_urls)

    def create_url_for_path(self, path):
        """Creates url to image with given path"""
        return self.api.url_for(ImageRepository, name=path, _external=True)

    @classmethod
    def create_json_response(cls, urls):
        json = jsonify(images=urls)
        return make_response(json, 200)

