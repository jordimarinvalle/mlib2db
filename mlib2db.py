#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

import redis

from textwrap import dedent

from mlib2db.file import File
from mlib2db.tune import Tune
from mlib2db.image import Image

from mlib2db.db.redis.mlib2rds import Albums as RdsAlbums, Album as RdsAlbum, \
    Tunes as RdsTunes, Tune as RdsTune, Images as RdsImages, Image as RdsImage

try:
    #mlit_path: music-library-tunes-path #mlii_path: music-library-images-path
    mlit_path, mlii_path = unicode(sys.argv[1]), unicode(sys.argv[2])
    if not os.path.exists(mlit_path) or not mlii_path: raise OSError()
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

tunes_key = RdsTunes.get_key()
images_key = RdsImages.get_key()
albums_key = RdsAlbums.get_key()

for (path, dirs, files) in os.walk(mlit_path):
    files = [os.path.join(path, f) for f in files]

    tunes = []
    images = []
    for f in files:
        file_type = File.get_mlibfile_type(File.get_mimetype(f))

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

    album   = flat_d['album'][0]
    artist  = 'VA' if len(flat_d['artist']) is not 1 else flat_d['artist'][0]
    genre   = '' if len(flat_d['genre']) is not 1 else flat_d['genre'][0]
    year    = '' if len(flat_d['year']) is not 1 else flat_d['year'][0]

    album_id3 = {'album': album, 'artist': artist, 'genre': genre, 'year': year}

    album_key = RdsAlbum.get_key(artist, album)
    album_id3_key = RdsAlbum.get_id3_key(album_key)
    for key, value in album_id3.iteritems():
        redis.hset(album_id3_key, key, value)


    album_tunes_key = RdsAlbum.get_tunes_key(album_key)
    album_images_key = RdsAlbum.get_images_key(album_key)

    redis.sadd(albums_key, album_key)


    for tune in tunes:

        album, title, artist = tune.id3gw.get_album(), tune.id3gw.get_title(), tune.id3gw.get_artist()
        if not album or not title or not artist: continue #@todo log {{path}}...

        tune_key = RdsTune.get_key(album, title, artist)
        tune_id3_key = RdsTune.get_id3_key(tune_key)
        tune_audio_key = RdsTune.get_audio_key(tune_key)

        for key, value in tune.get_id3().iteritems():
            redis.hset(tune_id3_key, key, value)

        redis.zadd(album_tunes_key, tune_key, tune.id3gw.get_trackn())
        redis.sadd(tunes_key, tune_key) #track and add all tunes


    for image in images:

        if image.get_type() is image.get_undefined_type(): continue

        image_key = RdsImage.get_key(artist, album, image.get_type())
        image_filenameid_key = RdsImage.get_filenameid_key(image_key)
        image_type_key = RdsImage.get_type_key(image_key)
        image_dims_key = RdsImage.get_dims_key(image_key)

        image_filenameid = image.get_filename_id((album_id3['artist'], album_id3['album']), image.get_type())

        redis.sadd(album_images_key, image_key)

        redis.sadd(images_key, image_key) #track and add all images

        redis.set(image_filenameid_key, image_filenameid)
        redis.set(image_type_key, image.get_type())
        for key, value in image.get_dims().iteritems():
            redis.hset(image_dims_key, key, value)

        shutil.copyfile(image.get_f(), os.path.join(mlii_path, image_filenameid))

albums_keys = redis.smembers(albums_key)
tunes_keys = redis.smembers(tunes_key)
images_keys = redis.smembers(images_key)

print "On Redis DB are: %s albums, %s tunes, %s images" %(len(albums_keys), len(tunes_keys), len(images_keys))