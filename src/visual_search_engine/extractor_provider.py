import cv2


class ExtractorProvider:
    @classmethod
    def get_extractor(cls, params=None):
        """Returns proper features extractor depending on the params"""
        params = ExtractorProvider.process_params(params)
        algorithm = ExtractorProvider.get_algorithm(params)
        return getattr(cv2.xfeatures2d, algorithm + '_create')(**params)

    @classmethod
    def process_params(cls, params):
        """Returns params object or default params if None"""
        return params or {'algorithm': 'SIFT'}

    @classmethod
    def get_algorithm(cls, params):
        """Returns algorithm from config and removes algorithm entry from params object"""
        algorithm = params['algorithm']
        params.pop('algorithm')
        return algorithm
