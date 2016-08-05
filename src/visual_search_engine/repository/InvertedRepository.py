from visual_search_engine.repository.repository import Repository


# TODO
class InvertedRepository(Repository):
    def __init__(self, repository_path):
        Repository.__init__(self, repository_path)

    def find(self, histogram):
        pass

    def add(self, name, image, histogram):
        pass

    def remove(self, name):
        pass
