import os
import shutil
import tempfile
import unittest
from os import path

from visual_search_engine.repository.simple_repository import SimpleRepository
from visual_search_engine.utils import normalize_dir_path


class SimpleRepositoryTest(unittest.TestCase):
    TEST_IMAGE_1 = 'test_file_1.jpg'
    TEST_IMAGE_2 = 'test_file_2.jpg'

    @classmethod
    def setUpClass(cls):
        with open(cls.TEST_IMAGE_1, 'rb') as file1:
            cls.test_img_1 = file1.read()
        with open(cls.TEST_IMAGE_2, 'rb') as file2:
            cls.test_img_2 = file2.read()

    @classmethod
    def setUp(cls):
        cls.temp_root = tempfile.mkdtemp()

    @classmethod
    def tearDown(cls):
        shutil.rmtree(cls.temp_root)

    def test_create_empty_repository(self):
        repo_dir = path.join(self.temp_root, 'index')
        normalized_repo_dir = normalize_dir_path(repo_dir)
        repository = SimpleRepository(repo_dir)
        self.assertEqual(normalized_repo_dir, repository.repository_dir)
        self.assertTrue(not os.listdir(repository.repository_dir))

    def test_after_add_repository_has_one_element(self):
        repository = SimpleRepository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        self.assertEqual(self.TEST_IMAGE_1, next(iter(elements))[0])
        self.assertEqual([self.TEST_IMAGE_1], os.listdir(repository.repository_dir))

    def test_after_remove_repository_with_one_element_is_empty(self):
        repository = SimpleRepository(self.temp_root)
        repository.add(self.TEST_IMAGE_1, self.test_img_1, {})
        elements = repository.elements.items()
        self.assertEqual(1, len(elements))
        repository.remove(self.TEST_IMAGE_1)
        elements = repository.elements.items()
        self.assertEqual(0, len(elements))
        self.assertTrue(not os.listdir(repository.repository_dir))


if __name__ == '__main__':
    unittest.main()