from visual_search_engine import SearchEngineError


class ImgLoadError(SearchEngineError):
    """Raised if image can't be loaded from given path"""
    def __init__(self, path_to_file=None):
        if path_to_file:
            message = "Can't load file:'" + path_to_file + "'"
        else:
            message = "Can't load image from buffer"
        SearchEngineError.__init__(self, message)


class ImgSizeError(SearchEngineError):
    """Raised if image width or height is smaller than IMAGE_MIN_SIZE"""
    def __init__(self, path_to_file):
        message = "Image '" + path_to_file + "' is too small"
        SearchEngineError.__init__(self, message)
