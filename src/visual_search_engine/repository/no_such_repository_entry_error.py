from visual_search_engine.error import SearchEngineError


class NoSuchRepositoryEntryError(SearchEngineError):
    def __init__(self, name):
        message = "Image with name '" + name + "' doesn't exist in repository"
        SearchEngineError.__init__(self, message)