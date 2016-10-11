import logging

from visual_search_engine.bow import BOW
from visual_search_engine.extractor import ExtractorProvider
from visual_search_engine.matcher.matcher_provider import MatcherProvider


class BOWProvider:
    log = logging.getLogger('web.BOWProvider')

    @classmethod
    def get_bow(cls, vocabulary, extractor_params=None, matcher_params=None):
        extractor = ExtractorProvider.get_extractor(extractor_params)
        matcher = MatcherProvider.get_matcher(matcher_params)
        BOWProvider.log.info("Creating BOW for vocabulary of size " + str(len(vocabulary)))
        return BOW(vocabulary, matcher, extractor)
