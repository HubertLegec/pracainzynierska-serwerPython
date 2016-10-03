from visual_search_engine.ranker import SimpleRanker, TFIDFRanker


class RankerProvider:
    @classmethod
    def get_ranker(cls, params=None):
        params = params or cls.DEFAULT_PARAMS
        mode = params['mode']
        method = params['method']
        return cls.get_by_mode(mode, method)

    @classmethod
    def get_by_mode(cls, mode, method):
        if mode == 'SIMPLE':
            return SimpleRanker(method)
        elif mode == 'TFIDF':
            return TFIDFRanker(method)
        return None

    DEFAULT_PARAMS = {
        'mode': 'SIMPLE',
        'method': 'CHI_SQUARED_ALT'
    }
