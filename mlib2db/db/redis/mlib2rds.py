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

    @staticmethod
    def get_key(album):
        return Album.separator.join([Album.album_key, slugify(album)])

    @staticmethod
    def get_tunes_key(album):
        return Album.separator.join([Album.get_key(album), Album.tunes_key])

    @staticmethod
    def get_images_key(album):
        return Album.separator.join([Album.get_key(album), Album.images_key])


class Tune(Tunes):

    tune_key = 'tune'

    id3_key = 'id3'
    audio_key = 'audio'

    @staticmethod
    def get_key(album, title, artist):
        return Tune.separator.join(
            [Tune.tune_key, '.'.join([slugify(album), slugify(title), slugify(artist)])]
        )

    @staticmethod
    def get_id3_key(album, title, artist):
        return Tune.separator.join(
            [Tune.get_key(album, title, artist), Tune.id3_key]
        )

    @staticmethod
    def get_audio_key(album, title, artist):
        return Tune.separator.join(
            [Tune.get_key(album, title, artist), Tune.audio_key]
        )
