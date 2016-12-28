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
    TEST_IMAGE_1 = get_resource_path('test_images/test_file_1.jpg')
    TEST_IMAGE_2 = get_resource_path('test_images/test_file_2.jpg')

    @classmethod
    def setUpClass(cls):
        cls.test_img_1 = FileUtils.load_file_bytes(cls.TEST_IMAGE_1)
        cls.test_img_2 = FileUtils.load_file_bytes(cls.TEST_IMAGE_2)

    @classmethod
    def setUp(cls):
        cls.temp_root = tempfile.mkdtemp()

    @classmethod
    def tearDown(cls):
        shutil.rmtree(cls.temp_root)

    def test_create_empty_repository(self):
        repo_dir = path.join(self.temp_root, 'index')
        normalized_repo_dir = FileUtils.normalize_dir_path(repo_dir)
        repository = Repository(repo_dir)
        self.assertEqual(normalized_repo_dir, repository.repository_dir)
        self.assertTrue(not os.listdir(repository.repository_dir))

    def test_after_add_repository_has_one_element(self):
        repository = Repository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        elements = repository.elements.items()
        test_image_1_name = FileUtils.get_filename_from_path(self.TEST_IMAGE_1)
        self.assertEqual(1, len(elements))
        self.assertEqual(test_image_1_name, next(iter(elements))[0])
        self.assertEqual([test_image_1_name], os.listdir(repository.repository_dir))

    def test_after_remove_repository_with_one_element_is_empty(self):
        repository = Repository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        repository.remove(FileUtils.get_filename_from_path(self.TEST_IMAGE_1))
        elements = repository.elements.items()
        self.assertEqual(0, len(elements))
        self.assertTrue(not os.listdir(repository.repository_dir))

    def test_add_the_same_element_should_fail(self):
        repository = Repository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        self.assertRaises(DuplicatedRepositoryEntryError, repository.add, self.TEST_IMAGE_1, self.test_img_1, {})

    def test_find_should_return_all_elements(self):
        repository = Repository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        repository.add(self.TEST_IMAGE_2, self.test_img_1, {})
        elements = repository.elements.items()
        self.assertEqual(2, len(elements))
        self.assertEqual(elements, repository.get_all())

