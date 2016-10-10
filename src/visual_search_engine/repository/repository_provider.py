from visual_search_engine.repository.simple_repository import SimpleRepository


class RepositoryProvider:
    @classmethod
    def get_repository(cls, params):
        params = params or cls.DEFAULT_PARAMS
        type = cls.get_repository_type(params)
        return cls.get_by_type(type, params)

    @classmethod
    def get_repository_type(cls, params):
        repository = params['type']
        params.pop('type')
        return repository

    @classmethod
    def get_by_type(cls, type, params):
        if type == 'SIMPLE':
            return SimpleRepository(params['directory'])
        return None

    DEFAULT_PARAMS = {
        'type': 'SIMPLE',
        'directory': './index/'
    }
