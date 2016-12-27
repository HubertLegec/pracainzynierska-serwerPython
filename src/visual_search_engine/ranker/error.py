from visual_search_engine import SearchEngineError


class NoSuchRankerTypeError(SearchEngineError):
    def __init__(self, ranker_name):
        message = "Unsupported ranker type: '" + ranker_name + "'"
        SearchEngineError.__init__(self, message)


class UnsupportedComparisonMethodError(SearchEngineError):
    def __init__(self, method_name):
        message = "Unsupported comparison method: '" + method_name + "'"
        SearchEngineError.__init__(self, message)