from visual_search_engine.ranker import Ranker
import math


class TFIDFRanker(Ranker):
    """TF-IDF - term frequency - inverse document frequency
        It's method to evaluate how important is a word in a document.
    """

    def __init__(self, method='Chi-Squared-alt'):
        self.vector = []
        Ranker.__init__(self, method)

    def update(self, repository):
        vector_before_normalization = [sum(x) for x in repository.elements.values()]
        self.vector = TFIDFRanker._normalize_vector(vector_before_normalization)

    def rank(self, histogram, repository, limit):
        result = []
        for file_name, hist in repository.find(histogram):
            weighted_histogram = self._weight_histogram(hist)
            match_rate = Ranker.get_match_rate(weighted_histogram, hist, self.method)
            result.append((match_rate, file_name))
        return result

    def _weight_histogram(self, histogram):
        weighted_histogram = []
        for i, val in enumerate(histogram):
            weighted_histogram.insert(i, -val * math.log(self.vector[i], 10))
        return TFIDFRanker._normalize_vector(weighted_histogram)

    @classmethod
    def calculate_tf(cls, histogram, idx):
        return histogram[idx] / sum(histogram)

    @classmethod
    def calculate_idf(cls, repository, idx):
        occurrence_counter = 0
        for histogram in repository:
            if histogram[idx] > 0:
                occurrence_counter += 1
        return math.log10(len(repository) / occurrence_counter)

    @classmethod
    def calculate_tfidf(cls, repository, histogram, idx):
        return cls.calculate_tf(repository, histogram, idx) * cls.calculate_idf(repository, idx)

    @staticmethod
    def _normalize_vector(vector):
        vector_sum = sum(vector)
        return [val/vector_sum for val in vector]
