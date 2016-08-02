from flask_restful import Resource


class ImageWarehouse(Resource):
    def __init__(self, **kwargs):
        self.search_engine = kwargs['search_engine']

    def post(self, name):
        return None

    def get(self, name):
        return None

    def delete(self, name):
        return None

