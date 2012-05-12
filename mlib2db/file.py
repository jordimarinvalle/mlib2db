#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mimetypes

class File():

    f = ''
    info = {}

    def __init__(self, f):
        self.f = f
        self.set_info(f)

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
    def get_file_type(mimetype):
        if mimetype in File.get_audio_allowed_mimetypes(): return 'audio'
        if mimetype in File.get_image_allowed_mimetypes(): return 'image'
        return 'unknown'


    def get_file(self):
        return self.f


    def set_info(self, f):
        self.info = {'name': os.path.basename(f),
                     'path': os.path.dirname(f),
                     'size': os.path.getsize(f),
                     'mime': mimetypes.guess_type(f)[0],
                     'ext': os.path.splitext(f)[1][1:],
                     'type': File.get_file_type(File.get_mimetype(f))
        }


    def get_info(self):
        return self.info


    def get_info_name(self):
        return self.info['name']


    def get_info_path(self):
        return self.info['path']


    def get_info_size(self):
        return self.info['size']


    def get_info_mime(self):
        return self.info['mime']


    def get_info_ext(self):
        return self.info['ext']


    def get_info_type(self):
        return self.info['type']

