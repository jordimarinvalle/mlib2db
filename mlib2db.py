#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import redis

from textwrap import dedent

from mlib2db.file import File
from mlib2db.tune import Tune
from mlib2db.image import Image

from mlib2db.db.redis.mlib2rds import Albums as RdsAlbums, Album as RdsAlbum, Tunes as RdsTunes, Tune as RdsTune

try:
    mlib_path, i_path = unicode(sys.argv[1]), unicode(sys.argv[2])
    if not os.path.exists(mlib_path) or not i_path: raise OSError()
except (IndexError, OSError):
    sys.exit(dedent("""\
        __ARGUMENTS_REQUIRED__
        1. __MUSIC_LIBRARY_PATH__ Param. Path where the music is stored. e.g.: /music/library/
        2. __IMAGE_LIBRARY_PATH__ Param. Path where the images are going to be is stored. e.g.: /music/images/
    """))

try:
    redis = redis.Redis('127.0.0.1') #@todo. add a test connection function
except (Exception):
    sys.exit(dedent("""\
        __REDIS_DB_CONNECTION_FAILED__
        Redis db connection failed. Check Redis db connection settings.
    """))

albums_key = RdsAlbums.get_key()

print "albums_key: %s" %(albums_key,)
raw_input("")

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

    if len(flat_d['album']) is not 1: continue #@todo log {{path}}...


    album_key = RdsAlbum.get_key(flat_d['album'][0])
    album_tunes_key = RdsAlbum.get_tunes_key(flat_d['album'][0])
    album_images_key = RdsAlbum.get_images_key(flat_d['album'][0])

    print "album_key: %s" %(album_key,)
    print "album_tunes_key: %s" %(album_tunes_key,)
    print "album_images_key: %s" %(album_images_key,)
    raw_input("")

    #redis.set(albums_key, album_key)


    for tune in tunes:

        album, title, artist = tune.id3gw.get_album(), tune.id3gw.get_title(), tune.id3gw.get_artist()
        if not album or not title or not artist: continue #@todo log {{path}}...


        tune_key = RdsTune.get_key(album, title, artist)
        tune_id3_key = RdsTune.get_id3_key(album, title, artist)
        tune_audio_key = RdsTune.get_audio_key(album, title, artist)

        print "tune_key: %s" %(tune_key,)
        print "tune_key_id3: %s" %(tune_id3_key,)
        print "tune_audio_id3: %s" %(tune_audio_key,)
        raw_input("")

        #for key, value in tune.get_id3().iteritems():
        #    redis.hset(tune_id3_key, key, value)

        #redis.zadd(album_tunes_key, tune_key, tune.id3gw.get_trackn())

    raw_input("")

    for image in images:
        #raw_input(image.get_info())
        #raw_input(image.get_dims())
        #raw_input(image.get_type())
        pass

