import logging
from flask_restful import Resource, request
from flask import send_file, make_response, jsonify
from visual_search_engine.repository.no_such_repository_entry_error import NoSuchRepositoryEntryError
from visual_search_engine.repository.duplicated_repository_entry_error import DuplicatedRepositoryEntryError
from visual_search_engine.image_loader import ImgLoadError, ImgSizeError


class ImageRepository(Resource):

    def __init__(self, **kwargs):
        self.log = logging.getLogger('ImageRepository')
        self.search_engine = kwargs['search_engine']

    def post(self, name):
        self.log.info('Adding new image: ' + name)
        try:
            self.search_engine.add_new_image(request.data, name)
            json = jsonify(message='Image added')
            self.log.info('Image + ' + name + 'added to repository.')
            return make_response(json, 201)
        except DuplicatedRepositoryEntryError(name) as e:
            no_entry_json = jsonify(message=e.message)
            return make_response(no_entry_json, 409)
        except (ImgLoadError, ImgSizeError) as e:
            error_json = jsonify(message=e.message)
            return make_response(error_json, 400)

    def get(self, name):
        self.log.info('Get image request for: ' + name)
        return send_file(self.search_engine.repository.repository_dir + name, mimetype='image/jpeg')

    def delete(self, name):
        self.log.info('Removing image: ' + name)
        try:
            self.search_engine.repository.remove(name)
            self.log.info('Image ' + name + ' removed')
            return make_response('Image removed', 200)
        except NoSuchRepositoryEntryError as e:
            raise FileNotFoundError

