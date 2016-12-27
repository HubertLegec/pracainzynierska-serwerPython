

class SearchEngineError(Exception):
    def __init__(self, message=''):
        self.message = message
        Exception.__init__(self, message)

        def __repr__(self):
            return self.message

        __str__ = __repr__
