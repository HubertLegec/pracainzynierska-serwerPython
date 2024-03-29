from flask_restful import Resource
from flask import jsonify
import logging
import numpy


class VocabularyData(Resource):
    def __init__(self, **kwargs):
        self.vocabulary = kwargs['vocabulary']
        self.log = logging.getLogger('vse.VocabularyData')

    def get(self):
        self.log.info('Vocabulary: ' + numpy.array_str(self.vocabulary))
        vocabulary_list = [[v.item() for v in row] for row in self.vocabulary]
        row_length = len(self.vocabulary[0])
        size = len(self.vocabulary)
        json = jsonify(
            vocabulary=vocabulary_list,
            size=size,
            rowSize=row_length)
        self.log.info('vocabulary returned, size: ' + str(size))
        return json
