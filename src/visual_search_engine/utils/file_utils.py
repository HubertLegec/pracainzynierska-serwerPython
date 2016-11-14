import pickle
import shutil
import logging


def load(path):
    """Loads file content using pickle"""
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content


def save(path, data):
    """Saves data to file under given path using pickle"""
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def load_file_bytes(path):
    with open(path, 'rb') as f:
        content = f.read()
    f.close()
    return content


def save_file_bytes(path, data):
    with open(path, 'wb') as f:
        f.write(data)
    f.close()


def normalize_dir_path(path):
    """Normalizes path to end with slash"""
    if len(path) > 0 and path[-1] != '/':
        path += '/'
    return path


def remove_dir(dir_path):
    """Removes directory if exist"""
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        logging.info("Error during removing directory '" + dir_path + "'")
        return


def get_image_name_from_url(url):
    start_name_idx = url.rfind('/')
    if start_name_idx < 0:
        return url
    return url[start_name_idx + 1:]
