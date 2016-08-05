from visual_search_engine.error import SearchEngineError


class UnsupportedComparisonMethodError(SearchEngineError):
    def __init__(self, method_name):
        message = "Unsupported comparison method: '" + method_name + "'"
        SearchEngineError.__init__(self, message)