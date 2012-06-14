#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import PIL.Image as Pil

from slugify import slugify
from mlib2db.file import File

class Image(File):

    UNDEFINED_TYPE = 'undefined'

    THUMB_DEFAULT_DIMX = 150
    THUMB_DEFAULT_DIMY = 150
    THUMB_FILENAME_KEY = 'thumb'

    dims = {'x': None, 'y': None}
    type = ''

    thumb = None

    def __init__(self, f):
        File.__init__(self, f)
        self.set_dims(f)
        self.set_type(f)


    def set_dims(self, f):
        dims = Pil.open(f).size
        self.set_dimx(dims[0])
        self.set_dimy(dims[1])

    def set_dimx(self, x):
        self.dims['x'] = x


    def set_dimy(self, y):
        self.dims['y'] = y


    def get_dims(self):
        return self.dims


    def get_dimx(self):
        return self.dims['x']


    def get_dimy(self):
        return self.dims['y']


    def get_types_from_a_filename(self):
        return {'cover': ['cover', 'front'], 'back': ['back',]}


    def get_undefined_type(self):
        return self.UNDEFINED_TYPE


    def set_type(self, f):
        self.type = self.get_undefined_type()
        filename = os.path.basename(os.path.splitext(f)[0])
        for type, filenames  in self.get_types_from_a_filename().items():
            if filename in filenames:
                self.type = type
                break


    def get_type(self):
        return self.type


    def get_filename_id(self, (artist, album), type):
        return '.'.join([slugify('-'.join([artist, album, type])), self.get_file_ext()])


    def get_filename_thumb_key(self):
        return self.THUMB_FILENAME_KEY


    def get_filename_thumb_id(self, i, d):
        return '.'.join([slugify('-'.join([i, d, self.get_filename_thumb_key()])), self.get_file_ext()])


    def is_a_square_image(self):
        if (float(self.get_dimx())/float(self.get_dimy()) == 1):
            return True
        return False


    def get_thumb_default_dims(self):
        return (self.THUMB_DEFAULT_DIMX, self.THUMB_DEFAULT_DIMY)


    def set_thumb(self, dims, type='NEAREST'):
        try:
            if dims is (): dims = self.get_thumb_default_dims()
            image = Pil.open(self.get_file())
            return image.resize(dims[0], dims[1], Pil.type)
        except:
            raise ThumbException ()


    def get_thumb(self):
        return self.thumb

