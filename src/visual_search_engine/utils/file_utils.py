import pickle
import shutil
import logging
import os


class FileUtils:

    @classmethod
    def load(cls, path):
        """Loads file content using pickle"""
        with open(path, 'rb') as f:
            content = pickle.load(f)
        return content

    @classmethod
    def save(cls, path, data):
        """Saves data to file under given path using pickle"""
        with open(path, 'wb') as f:
            pickle.dump(data, f, pickle.DEFAULT_PROTOCOL)

    @classmethod
    def load_file_bytes(cls, path):
        """Loads binary data from file"""
        with open(path, 'rb') as f:
            content = f.read()
        f.close()
        return content

    @classmethod
    def save_file_bytes(cls, path, data):
        """Saves data to file in binary mode"""
        with open(path, 'wb') as f:
            f.write(data)
        f.close()

    @classmethod
    def normalize_dir_path(cls, path):
        """Normalizes path to end with slash"""
        if len(path) > 0 and path[-1] != '/':
            path += '/'
        return path

    @classmethod
    def remove_dir(cls, dir_path):
        """Removes directory if exist"""
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            logging.info("Error during removing directory '" + dir_path + "'")
            return

    @classmethod
    def get_filename_from_path(cls, path):
        return os.path.basename(path)

    @classmethod
    def get_dir_from_filename(cls, filename):
        return os.path.dirname(filename)
