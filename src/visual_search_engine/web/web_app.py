from flask import Flask, jsonify, request
from flask_restful import Api
from . import Searcher
from . import ImageRepository
from . import VocabularyData
from . import ExtractorData
from . import MatcherData
from . import HistogramSearcher


app = Flask('Visual Search Engine')
api = Api(app)

NOT_FOUND_ERROR = 404


@app.errorhandler(NOT_FOUND_ERROR)
def not_found_handler(error):
    return jsonify(request.url + ' not found')


@app.route('/healthCheck')
def health_check():
    return 'OK'


def configure(search_engine, vocabulary, matcher):
    api.add_resource(VocabularyData, '/data/vocabulary',
                     resource_class_kwargs={'vocabulary': vocabulary})
    api.add_resource(ExtractorData, '/data/extractor',
                     resource_class_kwargs={'extractor': search_engine.bow.extractor})
    api.add_resource(MatcherData, '/data/matcher',
                     resource_class_kwargs={'matcher': matcher})
    api.add_resource(Searcher, '/find', '/find/<int:limit>',
                     resource_class_kwargs={'search_engine': search_engine, 'api': api})
    api.add_resource(HistogramSearcher, '/findByHist', '/findByHist/<int:limit>',
                     resource_class_kwargs={'search_engine': search_engine, 'api': api})
    api.add_resource(ImageRepository, '/upload/<path:name>',
                     resource_class_kwargs={'search_engine': search_engine})
    return app


def start(search_engine, vocabulary, matcher, host='127.0.0.1', port=5000, debug=False):
    application = configure(search_engine, vocabulary, matcher)
    application.run(host, port, debug)
