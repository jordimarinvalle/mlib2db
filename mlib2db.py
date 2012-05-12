#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from textwrap import dedent

from mlib2db.file import File
from mlib2db.tune import Tune
from mlib2db.image import Image

try:
    mlib_path, i_path = unicode(sys.argv[1]), unicode(sys.argv[2])
    if not os.path.exists(mlib_path) or not i_path: raise OSError()
except (IndexError, OSError):
    sys.exit(dedent("""\
        __ARGUMENTS_REQUIRED__
        1. __MUSIC_LIBRARY_PATH__ Param. Path where the music is stored. e.g.: /music/library/
        2. __IMAGE_LIBRARY_PATH__ Param. Path where the images are going to be is stored. e.g.: /music/images/
    """))

for (path, dirs, files) in os.walk(mlib_path):
    files = [os.path.join(path, f) for f in files]

    tunes = []
    images = []
    for f in files:
        file_type = File.get_file_type(File.get_mimetype(f))

        if file_type is 'audio':
            tunes.append(Tune(f))
            continue

        if file_type is 'image':
            images.append(Image(f))
            continue

    if len(tunes) is 0: continue #@todo log {{path}}...

    flat_d = {}
    for tune in tunes:
        flat_d = tune.flat_d(tune.get_id3(), flat_d)
    print flat_d

    do_debug = raw_input("Check tunes and images?: ")
    if not do_debug: continue

    for tune in tunes:
        raw_input(tune.get_info())
        raw_input(tune.get_id3())
        raw_input(tune.get_audio())

    for image in images:
        raw_input(image.get_info())
        raw_input(image.get_dims())
        raw_input(image.get_type())

