from visual_search_engine.error import SearchEngineError


class NoSuchRankerTypeError(SearchEngineError):
    def __init__(self, ranker_name):
        message = "Unsupported ranker type: '" + ranker_name + "'"
        SearchEngineError.__init__(self, message)
