import unittest

from tests.utils import get_object_name_with_package
from visual_search_engine import RepositoryProvider
from visual_search_engine.repository.no_such_repository_type_error import NoSuchRepositoryTypeError


class RepositoryProviderTest(unittest.TestCase):
    def test_get_default_repository(self):
        repository = RepositoryProvider.get_repository()
        repository_name = get_object_name_with_package(repository)
        directory = repository.repository_dir
        self.assertEqual('visual_search_engine.repository.simple_repository.SimpleRepository', repository_name)
        self.assertEqual('./index/', directory)

    def test_get_unknown_repository_cause_error(self):
        config = {
            'type': 'SOME_TYPE',
            'directory': '/dir/'
        }
        self.assertRaises(NoSuchRepositoryTypeError, RepositoryProvider.get_repository, config)

if __name__ == '__name__':
    unittest.main()