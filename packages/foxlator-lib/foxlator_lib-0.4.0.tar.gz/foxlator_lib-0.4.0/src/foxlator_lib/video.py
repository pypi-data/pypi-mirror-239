import pathlib

import moviepy.editor as mp  # type: ignore

from .audio import AudioPath
from .utils import FileSystem
from .error import BaseError


class VideoError(BaseError):
    pass


class Video(object):
    known_extensions = ['.mp4']

    def __init__(self, path: str, fs: FileSystem = FileSystem()):
        self.path = path
        self.fs = fs

        self._validate_extension(path)

        if (not self.fs.is_file(path)):
            raise VideoError(f"Video file: '{path}' doesn't exist")
        self.clip: mp.VideoFileClip = mp.VideoFileClip(self.path)

    def get_audio_path(self) -> AudioPath:
        if self.clip.audio:
            return AudioPath(audio=self.clip.audio)
        raise VideoError(reason="Clip doesn't have audio path")

    def _validate_extension(self, path: str):
        extension: str = pathlib.Path(path).suffix
        if len(extension) == 0:
            raise VideoError(
                "Provided file path is invalid or doesn't contain extension")
        if extension not in self.known_extensions:
            raise VideoError(f"Unsupported file extension: {extension}")
