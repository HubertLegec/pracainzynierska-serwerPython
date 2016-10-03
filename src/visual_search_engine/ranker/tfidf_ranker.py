from visual_search_engine.ranker.ranker import Ranker


class TFIDFRanker(Ranker):
    """TF-IDF - term frequency - inverse document frequency
        It's method to evaluate how important is a word in a document.
    """

    def __init__(self, method='Chi-Squared-alt'):
        self.vector = []
        Ranker.__init__(self, method)

    def update(self, repository):
        # TODO
        pass

    def rank(self, histogram, repository, limit):
        # TODO
        pass
