import cv2


class MatcherProvider:
    @classmethod
    def get_matcher(cls, params=None):
        params = params or cls.DEFAULT_FLANN__PARAMS
        matcher_type = cls.get_matcher_type(params)
        return getattr(cv2, matcher_type)(**params)

    @classmethod
    def get_matcher_type(cls, params):
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
