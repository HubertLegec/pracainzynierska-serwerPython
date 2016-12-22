import cv2
import logging


class ExtractorProvider:
    log = logging.getLogger('web.ExtractorProvider')

    @classmethod
    def get_extractor(cls, params=None):
        """Returns proper features extractor depending on the params"""
        params = ExtractorProvider.process_params(params)
        cls.log.info('get extractor of type: ' + params['algorithm'])
        algorithm = ExtractorProvider.get_algorithm(params)
        return getattr(cv2.xfeatures2d, algorithm + '_create')(**params)

    @classmethod
    def process_params(cls, params):
        """Returns params object or default params if None"""
        cls.log.warning('extractor not configured, default will be used: SIFT')
        return params or {'algorithm': 'SIFT'}

    @classmethod
    def get_algorithm(cls, params):
        """Returns algorithm from config and removes algorithm entry from params object"""
        algorithm = params['algorithm']
        params.pop('algorithm')
        return algorithm
