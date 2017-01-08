import os
import shutil
import tempfile
import unittest
from os import path

from .utils import get_resource_path
from visual_search_engine.repository import DuplicatedRepositoryEntryError
from visual_search_engine.repository import Repository
from visual_search_engine.utils import FileUtils


class RepositoryTest(unittest.TestCase):
    TEST_IMAGE_1 = 'test_file_1.jpg'
    TEST_IMAGE_2 = 'test_images/test_file_2.jpg'

    @classmethod
    def setUp(cls):
        cls.temp_root = tempfile.mkdtemp()

    def test_create_empty_repository(self):
        repository = Repository()
        self.assertEqual(None, repository.mongo)
        self.assertFalse(repository.loaded)
        self.assertEqual(0, len(repository.elements))

    def test_after_add_repository_has_one_element(self):
        repository = Repository()
        repository.loaded = True
        repository.add(self.TEST_IMAGE_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        self.assertEqual(self.TEST_IMAGE_1, next(iter(elements))[0])

    def test_add_the_same_element_should_fail(self):
        repository = Repository()
        repository.add(self.TEST_IMAGE_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        self.assertRaises(DuplicatedRepositoryEntryError, repository.add, self.TEST_IMAGE_1, {})

    def test_get_all_should_return_all_elements(self):
        repository = Repository()
        repository.loaded = True
        repository.add(self.TEST_IMAGE_1, {})
        repository.add(self.TEST_IMAGE_2, {})
        elements = repository.elements.items()
        self.assertEqual(2, len(elements))
        self.assertEqual(elements, repository.get_all())

