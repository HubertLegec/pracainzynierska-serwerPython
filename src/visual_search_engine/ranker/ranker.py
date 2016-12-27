import cv2
import heapq
import logging
from abc import ABC, abstractmethod
from scipy.spatial import distance
from . import UnsupportedComparisonMethodError


OPENCV_COMPARISON_METHODS = {
    'CORRELATION': cv2.HISTCMP_CORREL,
    'CHI_SQUARED': cv2.HISTCMP_CHISQR,
    'INTERSECTION': cv2.HISTCMP_INTERSECT,
    'HELLINGER': cv2.HISTCMP_HELLINGER,
    'BHATTACHARAYYA': cv2.HISTCMP_BHATTACHARYYA,
    'CHI_SQUARED_ALT': cv2.HISTCMP_CHISQR_ALT,
    'KULLBACK-LEIBLER': cv2.HISTCMP_KL_DIV
}

SCIPY_COMPARISON_METHODS = {
    'EUCLIDEAN': distance.euclidean,
    'CHEBYSEV': distance.chebyshev
}


class Ranker(ABC):
    def __init__(self, method='SIMPLE'):
        self.method = method
        self.log = logging.getLogger('vse.Ranker')

    @abstractmethod
    def rank(self, histogram, repository, limit):
        """Ranks images in index based on similarity to given histogram.
            :return list of tuples: (ratio, filename)
        """
        pass

    @abstractmethod
    def update(self, repository):
        """Should be invoked after image index change - ranker parameters update
            :param repository
        """
        pass

    def get_limited_result(self, result, limit):
        if self.method == 'CORRELATION' or self.method == 'INTERSECTION':
            self.log.info('Get limited result: ' + str(limit) + ' largest')
            return heapq.nlargest(limit, result, key=lambda pair: pair[0])
        else:
            self.log.info('Get limited result: ' + str(limit) + ' smallest')
            return heapq.nsmallest(limit, result, key=lambda pair: pair[0])

    @staticmethod
    def get_match_rate(reference_histogram, found_histogram, method):
        if method in OPENCV_COMPARISON_METHODS:
            return cv2.compareHist(reference_histogram, found_histogram, OPENCV_COMPARISON_METHODS[method])
        elif method in SCIPY_COMPARISON_METHODS:
            return SCIPY_COMPARISON_METHODS[method](reference_histogram, found_histogram)
        else:
            raise UnsupportedComparisonMethodError(method)


