from flask_restful import Resource
from flask import make_response, jsonify
import logging


class MatcherData(Resource):
    def __init__(self, **kwargs):
        self.matcher = kwargs['matcher']
        self.log = logging.getLogger('MatcherData')

    def get(self):
        json = jsonify(matcher=self.matcher)
        self.log.info('Matcher data request')
        return json

