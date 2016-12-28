from . import Ranker
import math


class TFIDFRanker(Ranker):
    """
    TF-IDF - term frequency - inverse document frequency
    It's method to evaluate how important is a word in a document.
    In computer vision and image recognition it is used to determine how important each visual word is among others,
    after that we can assign weights to words and use it when histograms are compared
    """

    def __init__(self, method='Chi-Squared-alt'):
        self.vector = []
        Ranker.__init__(self, method)

    def update(self, repository):
        repository_values = repository.elements.values()
        self.vector = [self._get_normalized_tfidf_hist(repository, hist) for hist in repository_values]

    def rank(self, histogram, repository, limit):
        result = []
        for file_name, hist in repository.get_all():
            weighted_histogram = self._weight_histogram(hist, repository)
            match_rate = self._get_match_rate(weighted_histogram, hist, self.method)
            result.append((match_rate, file_name))
        limited_result = self._get_limited_result(result, limit)
        return limited_result

    @classmethod
    def _get_normalized_tfidf_hist(cls, repository, histogram):
        return cls._normalize_vector(cls._calculate_histogram_tfidf(repository, histogram))

    @classmethod
    def _weight_histogram(cls, histogram, repository):
        weighted_histogram = cls._calculate_histogram_tfidf(repository, histogram)
        return cls._normalize_vector(weighted_histogram)

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
