#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mimetypes

class File():

    f = ''
    file = {}

    def __init__(self, f):
        self.f = f
        self.set_file(f)

    @staticmethod
    def get_mimetype(f):
        return mimetypes.guess_type(f)[0]


    @staticmethod
    def get_audio_allowed_mimetypes():
        return ('audio/mpeg', 'audio/ogg',)


    @staticmethod
    def get_image_allowed_mimetypes():
        return ('image/jpeg',)


    @staticmethod
    def get_mlibfile_type(mimetype):
        if mimetype in File.get_audio_allowed_mimetypes(): return 'audio'
        if mimetype in File.get_image_allowed_mimetypes(): return 'image'
        return 'unknown'


    def get_f(self):
        return self.f


    def set_file(self, f):
        self.file = {
            'name': os.path.basename(f),
            'path': os.path.dirname(f),
            'size': os.path.getsize(f),
            'mime': mimetypes.guess_type(f)[0],
            'ext': os.path.splitext(f)[1][1:],
            'type': File.get_mlibfile_type(File.get_mimetype(f)),
        }


    def get_file(self):
        return self.file


    def get_file_name(self):
        return self.file['name']


    def get_file_path(self):
        return self.file['path']


    def get_file_size(self):
        return self.file['size']


    def get_file_mime(self):
        return self.file['mime']


    def get_file_ext(self):
        return self.file['ext']


    def get_file_type(self):
        return self.file['type']

