import logging

from . import ExtractorProvider
from . import MatcherProvider
from . import BOW


class BOWProvider:
    log = logging.getLogger('vse.BOWProvider')

    @classmethod
    def get_bow(cls, vocabulary, extractor_params=None, matcher_params=None):
        extractor = ExtractorProvider.get_extractor(extractor_params)
        matcher = MatcherProvider.get_matcher(matcher_params)
        vocabulary_size = str(len(vocabulary))
        cls.log.info("Creating BOW for vocabulary of size " + vocabulary_size)
        return BOW(vocabulary, matcher, extractor)
