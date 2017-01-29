import logging
from . import Ranker


class SimpleRanker(Ranker):
    """Ranker with no custom logic.
    It doesn't store any custom data and doesn't use any additional parameters.
    When images are ranked theirs histograms are compared and best matches are returned."""
    def __init__(self, method='CHI_SQUARED_ALT'):
        Ranker.__init__(self, method)
        self.log = logging.getLogger('vse.SimpleRanker')

    def update(self, repository):
        pass

    def rank(self, histogram, repository, limit):
        self.log.info('rank repository images against histogram')
        result = []
        for file_name, hist in repository.get_all():
            match_rate = Ranker._get_match_rate(histogram, hist, self.method)
            self.log.debug('For image: ' + file_name + ' match rate: ' + str(match_rate))
            result.append((match_rate, file_name))
        limited_result = self._get_limited_result(result, limit)
        return limited_result

