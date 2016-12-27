import logging
import numpy
from flask import request, json
from . import BaseSearcher


class HistogramSearcher(BaseSearcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log = logging.getLogger('vse.HistogramSearcher')

    def post(self, limit=4):
        """Returns list of urls to images that matches payload, size of list is limited by <limit>"""
        self.log.info('histogram search with limit' + str(limit))
        histogram = HistogramSearcher.json_to_numpy_array(request.data)
        img_paths = self.search_engine.find_by_histogram(histogram, limit)
        self.log.info('search result size: ' + str(len(img_paths)))
        img_descriptions = self.create_images_descriptions(img_paths)
        return self.create_json_response(img_descriptions)

    @classmethod
    def json_to_numpy_array(cls, json_request):
        data = json.loads(json_request)
        return numpy.array(data, numpy.float32)

