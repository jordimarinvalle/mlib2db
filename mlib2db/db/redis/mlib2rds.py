#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slugify import slugify

class Core:

    separator = ":"


class Albums(Core):

    albums_key = 'albums'

    @staticmethod
    def get_key():
        return Albums.albums_key

class Tunes(Core):

    tunes_key = 'tunes'

    @staticmethod
    def get_key():
        return Tunes.tunes_key


class Images(Core):

    images_key = 'images'

    @staticmethod
    def get_key():
        return Images.images_key


class Album(Albums, Tunes, Images):

    album_key = 'album'

    id3_key = 'id3'
    audio_key = 'audio'

    @staticmethod
    def get_key(artist, album):
        return Album.separator.join(
            [Album.album_key, '.'.join([slugify(artist), slugify(album)])]
        )

    @staticmethod
    def get_id3_key(album_key):
        return Album.separator.join([album_key, Album.id3_key])

    @staticmethod
    def get_audio_key(album_key):
        return Album.separator.join([album_key, Album.audio_key])

    @staticmethod
    def get_tunes_key(album_key):
        return Album.separator.join([album_key, Album.tunes_key])

    @staticmethod
    def get_images_key(album_key):
        return Album.separator.join([album_key, Album.images_key])


class Tune(Core):

    tune_key = 'tune'

    id3_key = 'id3'
    audio_key = 'audio'

    @staticmethod
    def get_key(album, title, artist):
        return Tune.separator.join(
            [Tune.tune_key, '.'.join([slugify(album), slugify(title), slugify(artist)])]
        )

    @staticmethod
    def get_id3_key(tune_key):
        return Tune.separator.join([tune_key, Tune.id3_key])

    @staticmethod
    def get_audio_key(tune_key):
        return Tune.separator.join([tune_key, Tune.audio_key])

class Image(Core):

    image_key = 'image'

    @staticmethod
    def get_key(artist, album, type):
        return Image.separator.join([Image.image_key, '.'.join([slugify(artist), slugify(album), slugify(type)])])

