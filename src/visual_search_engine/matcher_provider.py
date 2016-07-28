import cv2


class MatcherProvider:
    @classmethod
    def get_matcher(cls, matcher_type='FlannBasedMatcher', params=None):
        params = params or cls.DEFAULT_FLANN__PARAMS
        return getattr(cv2, matcher_type)(**params)

    DEFAULT_FLANN__PARAMS = {
        'normType': cv2.NORM_L2,
        'searchParams': {},
        'indexParams': dict(algorithm=0, trees=5)
    }
