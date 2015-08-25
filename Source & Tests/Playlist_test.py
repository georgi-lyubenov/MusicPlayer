from Playlist import Playlist
from Song import Song

import unittest
import mock


class PlaylistTest(unittest.TestCase):
    def setUp(self):
        self.playlist = Playlist("MyPlaylist")
        self.song1 = Song("TestTitle", "TestArtist",
                          "TestAlbum", 3, 200, 128, "")
        self.playlist.add_song(self.song1)

    def test_init(self):
        self.assertEqual(self.playlist.name, "MyPlaylist")

    def test_get_all_songs(self):
        self.assertEqual(self.playlist.get_all_songs(), [self.song1])

    def test_get_first_song(self):
        self.assertEqual(self.playlist.get_first_song(), self.song1)

    def test_add_song(self):
        self.song2 = Song("It's My Life", "Bon Jovi",
                          "Unknown Album", 5, 200, 192, "")
        self.playlist.add_song(self.song2)
        self.assertEqual(
            [self.song1, self.song2], self.playlist.get_all_songs())

    def test_remove_song(self):
        with mock.patch('builtins.input', return_value=1):
            self.assertEqual(
                self.playlist.get_first_song().title, 'TestTitle')

    def test_rate_songs(self):
        with mock.patch('builtins.input', return_value=3):
            self.assertEqual(
                self.playlist.get_first_song().rating, 3)

    def test_remove_disrated(self):
        with mock.patch('builtins.input', return_value=4):
            self.assertEqual(self.playlist.get_all_songs(), [self.song1])


if __name__ == '__main__':
    unittest.main()
