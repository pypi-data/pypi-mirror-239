
import moviepy.editor as mp  # type: ignore


class AudioPath(object):
    def __init__(self, audio: mp.AudioFileClip):
        self.audio = audio

    def save(self, path: str):
        # TODO: consider taking codec/extensions as parameter instead of using .mp3
        self.audio.write_audiofile(path + '.mp3', logger=None)
