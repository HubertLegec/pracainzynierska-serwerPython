from visual_search_engine.error import SearchEngineError


class DuplicatedRepositoryEntryError(SearchEngineError):
    def __init__(self, name):
        message = "Image with name '" + name + "' already exists in repository"
        SearchEngineError.__init__(self, message)



