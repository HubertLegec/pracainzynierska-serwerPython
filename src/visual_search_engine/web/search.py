import logging
from flask_restful import Resource
from flask import request, jsonify
from . import ImageRepository


class Searcher(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']
        self.api = kwargs['api']
        self.log = logging.getLogger('Searcher')

    def post(self, limit=4):
        """Returns list of urls to images that matches payload, size of list is limited by <limit>"""
        query_file = request.files['image'].read()
        # --- for test: save last query image in app dir ---
        #with open('queryImg.jpg', 'wb') as w:
        #    w.write(query_file)
        result = self.search_engine.find(query_file, limit)
        img_descriptions = [self.create_image_description(entry) for entry in result]
        return Searcher.create_json_response(img_descriptions)

    def create_url_for_path(self, path):
        """Creates url to image with given path"""
        return self.api.url_for(ImageRepository, name=path, _external=True)

    def create_image_description(self, result_entry):
        rate = result_entry[0]
        url = self.create_url_for_path(result_entry[1])
        name = url[(url.rindex('/') + 1):url.rindex('.')]
        return {
            'url': url,
            'matchRate': rate,
            'name': name
        }

    @classmethod
    def create_json_response(cls, urls):
        json = jsonify(images=urls)
        return json

