import os


def get_object_name_with_package(obj):
    return obj.__class__.__module__ + '.' + type(obj).__name__


def get_image_name_from_url(url):
    start_name_idx = url.rfind('/')
    if start_name_idx < 0:
        return url
    return url[start_name_idx + 1:]


def get_resource_file(name):
    path = get_resource_path(name)
    with open(path, 'rb') as f:
        file = f.read()
    f.close()
    return file


def get_resource_path(name):
    dir_name = os.path.dirname(__file__)
    return os.path.join(dir_name, name)