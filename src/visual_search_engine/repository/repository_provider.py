import logging

from . import NoSuchRepositoryTypeError
from . import SimpleRepository


class RepositoryProvider:
    log = logging.getLogger('vse.RepositoryProvider')

    @classmethod
    def get_repository(cls, params=None):
        params = params or cls.DEFAULT_PARAMS
        repository_type = cls.get_repository_type(params)
        cls.log.info('Create repository of type ' + repository_type + ' in directory: ' + params['directory'])
        return cls._get_by_type(repository_type, params)

    @classmethod
    def get_repository_type(cls, params):
        repository = params['type']
        params.pop('type')
        return repository

    @classmethod
    def _get_by_type(cls, type, params):
        if type == 'SIMPLE':
            return SimpleRepository(params['directory'])
        else:
            raise NoSuchRepositoryTypeError(type)

    DEFAULT_PARAMS = {
        'type': 'SIMPLE',
        'directory': './index/'
    }
