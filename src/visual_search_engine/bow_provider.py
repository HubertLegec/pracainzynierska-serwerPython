import visual_search_engine
import logging


class BOWProvider:
    log = logging.getLogger('web.BOWProvider')

    @classmethod
    def get_bow(cls, vocabulary, extractor_params=None, matcher_params=None):
        extractor = visual_search_engine.ExtractorProvider.get_extractor(extractor_params)
        matcher = visual_search_engine.MatcherProvider.get_matcher(matcher_params)
        BOWProvider.log.info("Creating BOW for vocabulary of size " + str(len(vocabulary)))
        return visual_search_engine.BOW(vocabulary, matcher, extractor)
