from flask_restful import Resource
from flask import jsonify
from . import ImageRepository


class BaseSearcher(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']
        self.api = kwargs['api']

    def create_url_for_path(self, path):
        """Creates url to image with given path"""
        return self.api.url_for(ImageRepository, name=path, _external=True)

    def create_images_descriptions(self, result):
        return [self.create_image_description(entry) for entry in result]

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
