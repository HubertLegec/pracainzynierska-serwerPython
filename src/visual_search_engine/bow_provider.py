import visual_search_engine


class BOWProvider:
    @classmethod
    def get_bow(cls, vocabulary, algorithm=None, matcher=None, extractor_params=None, matcher_params=None):
        extractor = visual_search_engine.ExtractorProvider.get_extractor(algorithm, extractor_params)
        matcher = visual_search_engine.MatcherProvider.get_matcher(matcher, matcher_params)
        return visual_search_engine.BOW(vocabulary, matcher, extractor)
