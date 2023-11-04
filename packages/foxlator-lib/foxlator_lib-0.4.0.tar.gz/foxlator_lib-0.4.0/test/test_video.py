
from ddt import ddt, data  # type: ignore
from unittest.mock import patch

from utils import base
from src import foxlator_lib as fll


@ddt
class VideoTests(base.TestBase):
    invalid_paths = ['path-without-extension',
                     'path.mp3', 'path.jpg', 'relative/path/file.obj']

    def test_when_creating_video_from_not_existing_path_should_throw_error(self):
        path = 'some-path.mp4'
        with patch.object(fll.utils.FileSystem, 'is_file', return_value=False) as is_file_mock:
            fs = fll.utils.FileSystem()
            self.assertRaises(fll.video.VideoError,
                              lambda: fll.video.Video(path, fs))
            is_file_mock.assert_called_once_with(path)

    @data(*invalid_paths)
    def test_when_creating_video_from_path_with_not_supported_extensions_should_throw_error(self, path: str):
        with patch.object(fll.utils.FileSystem, 'is_file', return_value=None) as is_file_mock:
            fs = fll.utils.FileSystem()
            self.assertRaises(fll.video.VideoError,
                              lambda: fll.video.Video(path, fs))
            is_file_mock.assert_not_called()
