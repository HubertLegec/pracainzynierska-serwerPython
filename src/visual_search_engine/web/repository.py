from flask_restful import Resource, request
from flask import send_file, make_response, jsonify
from visual_search_engine.repository.error import NoSuchRepositoryEntryError, DuplicatedRepositoryEntryError
from visual_search_engine.web.web_app import not_found_handler
from visual_search_engine.image_loader.error import ImgLoadError, ImgSizeError


class ImageRepository(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']

    def post(self, name):
        try:
            self.search_engine.add_new_image(request.data, name)
            json = jsonify(message='Image added')
            return make_response(json, 201)
        except DuplicatedRepositoryEntryError(name) as e:
            no_entry_json = jsonify(message=e.message)
            return make_response(no_entry_json, 409)
        except (ImgLoadError, ImgSizeError) as e:
            error_json = jsonify(message=e.message)
            return make_response(error_json, 400)

    def get(self, name):
        return send_file(self.search_engine.repository.repository_dir + name, mimetype='image/jpeg')

    def delete(self, name):
        try:
            self.search_engine.repository.remove(name)
            json = jsonify(message='Image removed')
            return make_response(json, 200)
        except NoSuchRepositoryEntryError as e:
            return not_found_handler()

