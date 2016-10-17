from flask_restful import Resource
from flask import make_response, jsonify
import logging


class VocabularyData(Resource):
    def __init__(self, **kwargs):
        self.vocabulary = kwargs['vocabulary']
        self.log = logging.getLogger('VocabularyData')

    def get(self):
        vocabulary_list = [[v.item() for v in row] for row in self.vocabulary]
        json = jsonify(vocabulary=vocabulary_list)
        self.log.info('Vocabulary request')
        return make_response(json, 200)
