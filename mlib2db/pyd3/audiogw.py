"""
Mutagen package extension to make ID3 (http://en.wikipedia.org/wiki/ID3) 
life easier and a more readable code.

Abstract Mutagen layer to get tune audio info:
    - Bit Rate
    - Sample Rate
    - Format
    - Channels
    - ...
"""

import os

from mutagen.mp3 import MP3

class AudioGw():

    f = ""
    audio = None

    def __init__(self, f):
        self.f = f
        self.audio = self.open(f)

    def open(self, f):
        """
        Open an audio file to get audio file such as lenght, bitrate, version, layer, mode.

        Arguments:
        :param f: string e.g.: /path/to/file/file.mp3

        :return: mutagen MP3 object
        """
        return MP3(f)


    def get_audio(self):
        """
        Get basic audio file data such as lenght, bitrate, version, layer, mode.

        :return: dictionary
        """
        return {'length': self.get_length(),
            'bitrate': self.get_bitrate(),
            'version': self.get_version(),
            'layer': self.get_layer(),
            'mode': self.get_mode(),
        }


    def get_length(self):
        return self.audio.info.length


    def render_length(self):
        secs, sec = divmod(self.get_length(), 60)
        hr, min = divmod(secs, 60)
        return "%02d:%02d:%02d" %(hr, min, sec)


    def get_bitrate(self):
        return self.audio.info.bitrate


    def render_bitrate(self):
        return "%s kbps" %(self.get_bitrate()/1000)


    def get_version(self):
        return self.audio.info.version


    def render_version(self):
        return "MPG-%i" %(self.get_version())


    def get_layer(self):
        return self.audio.info.layer


    def render_layer(self):
        return "Layer %i" %(self.get_layer())


    def get_format(self):
        return (self.get_version(), self.get_layer())


    def render_format(self):
        return "%s, %s" %(self.get_version(), self.get_layer())


    def get_mode(self):
        options = {0: "Stereo",
                   1: "Joint Stereo",
                   2: "Dual Channel",
                   3: "Mono",
        }
        return options.get(self.audio.info.mode, "Unknown Mode")


    def render_mode(self):
        return self.get_mode()


    def get_samplerate(self):
        return self.audio.info.samplerate


    def render_samplerate(self):
        return "%s kHz" %(self.get_samplerate())
