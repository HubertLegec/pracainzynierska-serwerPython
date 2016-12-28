import logging

from . import SimpleRanker
from . import TFIDFRanker
from . import NoSuchRankerTypeError


class RankerProvider:
    log = logging.getLogger('vse.RankerProvider')

    @classmethod
    def get_ranker(cls, params=None):
        params = cls._process_params(params)
        mode = params['mode']
        method = params['method']
        return cls._get_by_mode(mode, method)

    @classmethod
    def _get_by_mode(cls, mode, method):
        if mode == 'SIMPLE':
            return SimpleRanker(method)
        elif mode == 'TFIDF':
            return TFIDFRanker(method)
        raise NoSuchRankerTypeError(mode)

    @classmethod
    def _process_params(cls, params):
        """Returns params object or default params if None"""
        if not params:
            cls.log.warning('ranker not configured, default will be used: SIMPLE')
        return params or cls.DEFAULT_PARAMS

    DEFAULT_PARAMS = {
        'mode': 'SIMPLE',
        'method': 'CHI_SQUARED_ALT'
    }
