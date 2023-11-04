
from .file_system import FileSystem


def get_version() -> str:
    import importlib.metadata
    return importlib.metadata.version('foxlator_lib')


__all__ = [
    'FileSystem', 'get_version'
]
