from visual_search_engine.error import SearchEngineError


class NoSuchRepositoryTypeError(SearchEngineError):
    def __init__(self, type):
        message = "Implementation of repository type:" + type + " is not implemented"
        SearchEngineError.__init__(self, message)
