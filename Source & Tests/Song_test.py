from Song import Song

import unittest


class SongTest(unittest.TestCase):
    def setUp(self):
        self.song = Song("TestTitle", "TestArtist",
                         "TestAlbum", 2, 200, 128, "")

    def test_init(self):
        self.assertEqual(self.song.title, "TestTitle")
        self.assertEqual(self.song.artist, "TestArtist")
        self.assertEqual(self.song.album, "TestAlbum")
        self.assertEqual(self.song.rating, 2)
        self.assertEqual(self.song.length, 200)
        self.assertEqual(self.song.bitrate, 128)
        self.assertEqual(self.song.path_to_file, "")

    def test_rate(self):
        self.song.rate(4)
        self.assertEqual(self.song.rating, 4)

    def test_get_artist(self):
        self.assertEqual(self.song.get_artist(), "TestArtist")

    def test_get_title(self):
        self.assertEqual(self.song.get_title(), "TestTitle")

    def test_get_album(self):
        self.assertEqual(self.song.get_album(), "TestAlbum")

    def test_get_rating(self):
        self.assertEqual(self.song.get_rating(), 2)

    def test_get_length(self):
        self.assertEqual(self.song.get_length(), 200)

    def test_get_bitrate(self):
        self.assertEqual(self.song.get_bitrate(), 128)

if __name__ == '__main__':
    unittest.main()
