import cv2


class MatcherProvider:
    @classmethod
    def get_matcher(cls, params=None):
        params = params or cls.DEFAULT_FLANN__PARAMS
        matcher_type = cls.get_matcher(params)
        return getattr(cv2, matcher_type)(**params)

    @classmethod
    def get_matcher(cls, params):
        matcher = params['matcherType']
        params.pop('matcherType')
        return matcher

    DEFAULT_FLANN__PARAMS = {
        'matcherType': 'FlannBasedMatcher',
        'normType': cv2.NORM_L2,
        'searchParams': {},
        'indexParams': dict(algorithm=0, trees=5)
    }
