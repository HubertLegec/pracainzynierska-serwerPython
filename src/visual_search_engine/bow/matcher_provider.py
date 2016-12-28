import cv2
import logging


class MatcherProvider:
    log = logging.getLogger('vse.MatcherProvider')

    @classmethod
    def get_matcher(cls, params=None):
        params = cls._process_params(params)
        params_copy = params.copy()
        matcher_type = cls._get_matcher_type(params_copy)
        return getattr(cv2, matcher_type)(**params_copy)

    @classmethod
    def _process_params(cls, params):
        """Returns params object or default params if None"""
        if not params:
            cls.log.warning('matcher not configured, default will be used: BFMatcher')
        return params or cls.DEFAULT_BF_PARAMS

    @classmethod
    def _get_matcher_type(cls, params):
        matcher = params['matcher_type']
        params.pop('norm_type')
        params.pop('matcher_type')
        return matcher

    DEFAULT_FLANN__PARAMS = {
        'matcher_type': 'FlannBasedMatcher',
        'norm_type': cv2.NORM_L2,
        'searchParams': {},
        'indexParams': dict(algorithm=0, trees=5)
    }

    DEFAULT_BF_PARAMS = {
        'matcher_type': 'BFMatcher',
        'norm_type': cv2.NORM_L2,
    }
