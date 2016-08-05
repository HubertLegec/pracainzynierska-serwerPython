import cv2
from abc import ABC, abstractmethod
from visual_search_engine.ranker.error import UnsupportedComparisonMethodError


OPENCV_METHODS = {
    'CORRELATION': cv2.HISTCMP_CORREL,
    'CHI_SQUARED': cv2.HISTCMP_CHISQR,
    'INTERSECTION': cv2.HISTCMP_INTERSECT,
    'HELLINGER': cv2.HISTCMP_HELLINGER,
    'BHATTACHARAYYA': cv2.HISTCMP_BHATTACHARYYA,
    'CHI_SQUARED_ALT': cv2.HISTCMP_CHISQR_ALT,
    'KULLBACK-LEIBLER': cv2.HISTCMP_KL_DIV
}


class Ranker(ABC):
    def __init__(self, method='SIMPLE'):
        self.method = method

    @abstractmethod
    def rank(self, histogram, repository, limit):
        pass

    @abstractmethod
    def update(self, repository):
        pass

    @staticmethod
    def get_match_rate(reference_histogram, found_histogram, method):
        if method in OPENCV_METHODS:
            return cv2.compareHist(reference_histogram, found_histogram, OPENCV_METHODS[method])
        else:
            raise UnsupportedComparisonMethodError(method)


