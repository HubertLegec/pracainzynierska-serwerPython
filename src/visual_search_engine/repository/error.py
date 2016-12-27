from visual_search_engine import SearchEngineError


class DuplicatedRepositoryEntryError(SearchEngineError):
    def __init__(self, name):
        message = "Image with name '" + name + "' already exists in repository"
        SearchEngineError.__init__(self, message)


class NoSuchRepositoryEntryError(SearchEngineError):
    def __init__(self, name):
        message = "Image with name '" + name + "' doesn't exist in repository"
        SearchEngineError.__init__(self, message)


class NoSuchRepositoryTypeError(SearchEngineError):
    def __init__(self, type):
        message = "Implementation of repository type:" + type + " is not implemented"
        SearchEngineError.__init__(self, message)