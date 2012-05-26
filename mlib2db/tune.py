#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyd3.id3gw import Id3Gw
from pyd3.audiogw import AudioGw

from mlib2db.file import File

class Tune(File):

    id3gw = None
    audiogw = None

    def __init__(self, f):
        self.set_file(f)
        self.set_audio(f)
        self.set_id3(f)


    def set_id3(self, f):
        self.id3gw = Id3Gw(f)


    def get_id3(self):
        return self.id3gw.get_id3()


    def set_audio(self, f):
        self.audiogw = AudioGw(f)


    def get_audio(self):
        return self.audiogw.get_audio()


    def flat_d(self, d, flat_d):
        for key, value in d.iteritems():
            if not flat_d.has_key(key):
                flat_d[key] = [value,]
            elif value not in flat_d[key]:
                flat_d[key].append(value)

        return flat_d
