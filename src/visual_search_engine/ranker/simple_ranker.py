from . import Ranker


class SimpleRanker(Ranker):
    def __init__(self, method='CHI_SQUARED_ALT'):
        Ranker.__init__(self, method)

    def update(self, repository):
        pass

    def rank(self, histogram, repository, limit):
        result = []
        for file_name, hist in repository.find(histogram):
            match_rate = Ranker.get_match_rate(histogram, hist, self.method)
            result.append((match_rate, file_name))
        limited_result = self.get_limited_result(result, limit)
        return limited_result

