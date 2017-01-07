from flask_restful import Resource
from flask import jsonify
from . import ImageRepository


class BaseSearcher(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']
        self.api = kwargs['api']

    def create_images_descriptions(self, result):
        return [self._create_image_description(entry) for entry in result]

    def _create_image_description(self, result_entry):
        rate = result_entry[0]
        file = result_entry[1]
        url = self._create_url_for_path(result_entry[1])
        description = self.search_engine.repository.get_description(file)
        return {
            'url': url,
            'matchRate': rate,
            'name': description['name'],
            'pageUrl': description['url']
        }

    def _create_url_for_path(self, path):
        return self.api.url_for(ImageRepository, file=path, _external=True)
