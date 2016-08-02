from visual_search_engine.error import SearchEngineError


class ImgLoadError(SearchEngineError):
    def __init__(self, path_to_file):
        message = "Can't load file:'" + path_to_file + "'"
        SearchEngineError.__init__(self, message)


class ImgSizeError(SearchEngineError):
    def __init__(self, path_to_file):
        message = "Image '" + path_to_file + "' is too small"
        SearchEngineError.__init__(self, message)
