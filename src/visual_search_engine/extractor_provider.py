import cv2


class ExtractorProvider:
    @classmethod
    def get_extractor(cls, algorithm='SIFT', params={}):
        return getattr(cv2.xfeatures2d, algorithm + '_create')(**params)