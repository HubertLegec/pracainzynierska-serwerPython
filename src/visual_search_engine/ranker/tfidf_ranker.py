from . import Ranker
import math
import numpy


class TFIDFRanker(Ranker):
    """
    TF-IDF - term frequency - inverse document frequency
    It's method to evaluate how important is a word in a document.
    In computer vision and image recognition it is used to determine how important each visual word is among others,
    after that we can assign weights to words and use it when histograms are compared
    """

    def __init__(self, method='Chi-Squared-alt'):
        self.elements = None
        Ranker.__init__(self, method)

    def update(self, repository):
        self.elements = {}
        repository_elements = repository.elements.items()
        for name, hist in repository_elements:
            self.elements[name] = self._get_normalized_tfidf_hist(repository, hist)

    def rank(self, histogram, repository, limit):
        if not self.elements:
            self.update(repository)
        result = []
        weighted_histogram = self._get_normalized_tfidf_hist(repository, histogram)
        for file_name, hist in self.elements.items():
            match_rate = self._get_match_rate(weighted_histogram, hist, self.method)
            result.append((match_rate, file_name))
        limited_result = self._get_limited_result(result, limit)
        return limited_result

    @classmethod
    def _get_normalized_tfidf_hist(cls, repository, histogram):
        weighted_histogram = cls._calculate_histogram_tfidf(repository, histogram)
        norm_vect = cls._normalize_vector(weighted_histogram)
        return numpy.asarray(norm_vect, dtype=numpy.float32)

    @classmethod
    def _calculate_tf(cls, histogram, idx):
        return histogram[idx] / sum(histogram)

    @classmethod
    def _calculate_idf(cls, repository, idx):
        occurrence_counter = 0
        for histogram in repository.elements.values():
            if histogram[idx] != 0:
                occurrence_counter += 1
        if occurrence_counter == 0:
            return 0
        return math.log10(len(repository.elements) / occurrence_counter)

    @classmethod
    def _calculate_tfidf(cls, repository, histogram, idx):
        return cls._calculate_tf(histogram, idx) * cls._calculate_idf(repository, idx)

    @classmethod
    def _calculate_histogram_tfidf(cls, repository, histogram):
        return [cls._calculate_tfidf(repository, histogram, i) for i, val in enumerate(histogram)]

    @classmethod
    def _normalize_vector(cls, vector):
        vector_sum = sum(vector)
        if vector_sum == 0:
            return vector
        return [val / vector_sum for val in vector]
