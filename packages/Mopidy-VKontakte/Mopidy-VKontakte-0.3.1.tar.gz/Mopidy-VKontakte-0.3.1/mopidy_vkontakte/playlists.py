# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import Playlist, Track, Artist
from urllib import unquote
logger = logging.getLogger(__name__)


class VKPlaylistsProvider(backend.PlaylistsProvider):

    def __init__(self, *args, **kwargs):
        super(VKPlaylistsProvider, self).__init__(*args, **kwargs)
        self.config = self.backend.config
        self._playlists = []
        self.all_lists = {}
        self.mopidy_playlists = {}

        self.refresh()
        self.filling_playlists()

    def create(self, name):
        pass

    def delete(self, uri):
        pass

    def _to_mopidy_track(self, song):
        return Track(
            uri=song['url'],
            name=unquote(song['title']),
            artists=[Artist(name=unquote(song['artist']))],
            length=int(song['duration']) * 1000
        )

    def lookup(self, uri):
        return self.all_lists[uri]

    def _vk_playlist_to_mopidy(self, playlist):
        logger.info(
            'Fetching a playlist "%s" from VKontakte'
            % playlist['title'])

        if playlist['title'] == 'all_songs':
            songs = self.backend.library.get_all_songs()
        else:
            songs = self.backend.library.get_all_songs_from_album(
                playlist['album_id'])

        tracks = []
        for song in songs:
            tracks.append(self._to_mopidy_track(song))

        return Playlist(
            uri='vkontakte:' + playlist['title'],
            name=playlist['title'],
            tracks=tracks
        )

    def filling_playlists(self):
        for list in self.all_lists:
            self.mopidy_playlists[list] = self.backend.library.tracklist_to_vfs(self.all_lists[list].tracks)

    def refresh(self):
        self.all_lists['vkontakte:all_songs'] = self._vk_playlist_to_mopidy(
            {'title': 'all_songs'})

        self._playlists.append(self.all_lists['vkontakte:all_songs'])

        vk_lists = self.backend.library.get_all_albums()
        for i in xrange(1, len(vk_lists)):
            title = 'vkontakte:' + vk_lists[i]['title']
            self.all_lists[title] = self._vk_playlist_to_mopidy(vk_lists[i])
            self._playlists.append(self.all_lists[title])

        logger.info(
            'Loaded' +
            ' {0} VKontakte playlist(s)'.format(len(self._playlists))
        )
        self.backend.library.generate_folders(self.all_lists)

        backend.BackendListener.send('playlists_loaded')

    def save(self, playlist):
        pass



