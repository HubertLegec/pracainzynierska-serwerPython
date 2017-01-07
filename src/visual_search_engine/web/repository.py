import logging
from flask_restful import Resource, request
from flask import make_response, jsonify
from visual_search_engine.repository import NoSuchRepositoryEntryError
from visual_search_engine.repository import DuplicatedRepositoryEntryError
from visual_search_engine.utils import ImgLoadError, ImgSizeError


class ImageRepository(Resource):

    def __init__(self, **kwargs):
        self.log = logging.getLogger('vse.ImageRepository')
        self.search_engine = kwargs['search_engine']

    def post(self, file, name):
        self.log.info('Adding new image: ' + file)
        try:
            image = request.files['upload'].read()
            self.search_engine.add_new_image(image, file, name)
            json = jsonify(message='Image added')
            self.log.info('Image ' + name + ' added to repository.')
            return json
        except DuplicatedRepositoryEntryError as e:
            no_entry_json = jsonify(message=e.message)
            return make_response(no_entry_json, 409)
        except (ImgLoadError, ImgSizeError) as e:
            error_json = jsonify(message=e.message)
            return make_response(error_json, 400)

    def get(self, file):
        self.log.info('Get image request for: ' + file)
        return self.search_engine.repository.get(file)

    def delete(self, file):
        self.log.info('Removing image: ' + file)
        try:
            self.search_engine.repository.remove(file)
            self.log.info('Image ' + file + ' removed')
            json = jsonify(message='Image removed')
            return json
        except NoSuchRepositoryEntryError as e:
            json = jsonify(message=e.message)
            return make_response(json, 404)

