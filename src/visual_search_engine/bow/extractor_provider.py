import cv2
import logging


class ExtractorProvider:
    log = logging.getLogger('vse.ExtractorProvider')

    @classmethod
    def get_extractor(cls, params=None):
        """Returns proper features extractor depending on the params"""
        params = cls._process_params(params)
        cls.log.info('get extractor of type: ' + params['algorithm'])
        algorithm = cls._get_algorithm(params)
        return getattr(cv2.xfeatures2d, algorithm + '_create')(**params)

    @classmethod
    def _process_params(cls, params):
        """Returns params object or default params if None"""
        if not params:
            cls.log.warning('extractor not configured, default will be used: SIFT')
        return params or {'algorithm': 'SIFT'}

    @classmethod
    def _get_algorithm(cls, params):
        """Returns algorithm from config and removes algorithm entry from params object"""
        algorithm = params['algorithm']
        params.pop('algorithm')
        if algorithm != 'SIFT':
            params.pop('nfeatures', None)
        return algorithm
