import os.path


class FileSystem(object):
    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)
