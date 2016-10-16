
def get_object_name_with_package(obj):
    return obj.__class__.__module__ + '.' + type(obj).__name__


def get_image_name_from_url(url):
    start_name_idx = url.rfind('/')
    if start_name_idx < 0:
        return url
    return url[start_name_idx + 1:]
