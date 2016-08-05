import visual_search_engine


class BOWProvider:
    @classmethod
    def get_bow(cls, vocabulary, extractor_params=None, matcher_params=None):
        extractor = visual_search_engine.ExtractorProvider.get_extractor(extractor_params)
        matcher = visual_search_engine.MatcherProvider.get_matcher(matcher_params)
        return visual_search_engine.BOW(vocabulary, matcher, extractor)
