
def get_object_name_with_package(obj):
    return obj.__class__.__module__ + '.' + type(obj).__name__
