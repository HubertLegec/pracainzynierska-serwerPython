from flask import Flask, jsonify, request
from flask_restful import Api
from .web import Searcher
from .web import ImageRepository
from .web import VocabularyData
from .web import ExtractorData
from .web import MatcherData
from .web import HistogramSearcher


app = Flask('Visual Search Engine')
app_configured = False


@app.errorhandler(FileNotFoundError)
def not_found_handler(error):
    return jsonify(request.url + ' not found')


@app.route('/healthCheck')
def health_check():
    return 'OK'


def configure(search_engine, vocabulary, matcher):
    global app_configured
    global app
    if not app_configured:
        api = Api(app)
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
        app_configured = True
    return app


def start(search_engine, vocabulary, matcher, host='127.0.0.1', port=5000, debug=False):
    application = configure(search_engine, vocabulary, matcher)
    application.run(host, port, debug)
