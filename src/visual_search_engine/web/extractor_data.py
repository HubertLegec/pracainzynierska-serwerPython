from flask_restful import Resource
from flask import jsonify
import logging


class ExtractorData(Resource):
    def __init__(self, **kwargs):
        self.extractor = ExtractorData.get_object_name_with_package(kwargs['extractor'])
        self.log = logging.getLogger('web.ExtractorData')

    def get(self):
        json = jsonify(extractor=self.extractor)
        self.log.info('Extractor data request')
        return json

    @classmethod
    def get_object_name_with_package(cls, obj):
        return obj.__class__.__module__ + '.' + type(obj).__name__
