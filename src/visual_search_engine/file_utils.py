import pickle


def load(path):
    """Loads file content using pickle"""
    with open(path, 'rb') as f:
        content = pickle.load(f)
    return content


def save(path, data):
    "Saves data to file under given path using pickle"
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
