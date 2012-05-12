#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import PIL.Image as pil

from mlib2db.file import File

class Image(File):

    THUMB_DEFAULT_DIMX = 150
    THUMB_DEFAULT_DIMY = 150

    dims = ()
    type = ''

    thumb = None

    def __init__(self, f):
        self.set_info(f)
        self.set_dims(f)
        self.set_type(f)


    def set_dims(self, f):
        self.dims = pil.open(f).size


    def get_dims(self):
        return self.dims


    def get_dimx(self):
        return self.dims[0]


    def get_dimy(self):
        return self.dims[1]


    def get_types_from_a_filename(self):
        return {'cover': ['cover', 'front'], 'back': ['back',]}


    def get_undefined_type(self):
        return 'undefined'


    def set_type(self, f):
        type = self.get_undefined_type()
        filename = os.path.basename(os.path.splitext(f)[0])
        types = self.get_types_from_a_filename()
        for type, filenames  in types.items():
            if filename in filenames:
                break
        self.type = type


    def get_type(self):
        return self.type


    def is_a_square_image(self):
        if (float(self.get_dimx())/float(self.get_dimy()) == 1):
            return True
        return False


    def get_thumb_default_dims(self):
        return (self.THUMB_DEFAULT_DIMX, self.THUMB_DEFAULT_DIMY)


    def set_thumb(self, dims, type='NEAREST'):
        try:
            if dims is (): dims = self.get_thumb_default_dims()
            image = pil.open(self.get_file())
            return image.resize(dims[0], dims[1], pil.type)
        except:
            raise ThumbException ()


    def get_thumb(self):
        return self.thumb

