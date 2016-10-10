from flask import Flask, jsonify, request, make_response
from flask_restful import Api
from visual_search_engine.web.search import Searcher
from visual_search_engine.web.repository import ImageRepository

app = Flask('Visual Search Engine')
api = Api(app)

NOT_FOUND_ERROR = 404


@app.errorhandler(NOT_FOUND_ERROR)
def not_found_handler():
    json = jsonify(request.url + ' not found')
    make_response(json, NOT_FOUND_ERROR)


def start(search_engine, host='127.0.0.1', port=9000, debug=False):
    api.add_resource(Searcher, '/find', '/find/<int:limit>',
                     resource_class_kwargs={'api': api, 'search_engine': search_engine})
    api.add_resource(ImageRepository, '/upload/<path:name>',
                     resource_class_kwargs={'api': api, 'search_engine': search_engine})
    app.run(host, port, debug)
