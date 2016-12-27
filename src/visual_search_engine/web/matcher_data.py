from flask_restful import Resource
from flask import jsonify
import logging


class MatcherData(Resource):
    def __init__(self, **kwargs):
        self.matcher = kwargs['matcher']
        self.log = logging.getLogger('vse.MatcherData')

    def get(self):
        json = jsonify(matcher=self.matcher)
        self.log.info('Matcher data request')
        return json

