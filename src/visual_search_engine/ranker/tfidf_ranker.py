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
        self.vector = [TFIDFRanker._normalize_vector(TFIDFRanker.calculate_histogram_tfidf(repository, histogram)) for histogram in
                       repository.elements.values()]

    def rank(self, histogram, repository, limit):
        result = []
        for file_name, hist in repository.get_all():
            weighted_histogram = TFIDFRanker._weight_histogram(hist, repository)
            match_rate = Ranker.get_match_rate(weighted_histogram, hist, self.method)
            result.append((match_rate, file_name))
        limited_result = self.get_limited_result(result, limit)
        return [pair[1] for pair in limited_result]

    @staticmethod
    def _weight_histogram(histogram, repository):
        weighted_histogram = TFIDFRanker.calculate_histogram_tfidf(repository, histogram)
        return TFIDFRanker._normalize_vector(weighted_histogram)

    @staticmethod
    def calculate_tf(histogram, idx):
        return histogram[idx] / sum(histogram)

    @staticmethod
    def calculate_idf(repository, idx):
        occurrence_counter = 0
        for histogram in repository.elements.values():
            if histogram[idx] != 0:
                occurrence_counter += 1
        if occurrence_counter == 0:
            return 0
        return math.log10(len(repository.elements) / occurrence_counter)

    @staticmethod
    def calculate_tfidf(repository, histogram, idx):
        return TFIDFRanker.calculate_tf(histogram, idx) * TFIDFRanker.calculate_idf(repository, idx)

    @staticmethod
    def calculate_histogram_tfidf(repository, histogram):
        return [TFIDFRanker.calculate_tfidf(repository, histogram, i) for i, val in enumerate(histogram)]

    @staticmethod
    def _normalize_vector(vector):
        vector_sum = sum(vector)
        if vector_sum == 0:
            return vector
        return [val / vector_sum for val in vector]
