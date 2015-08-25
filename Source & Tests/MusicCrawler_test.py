from Playlist import Playlist
from MusicCrawler import MusicCrawler
from MusicCrawler import session, MyPlaylist
import unittest


class MusicCrawlerTest(unittest.TestCase):
    def setUp(self):
        self.mc = MusicCrawler("MyCrawler", "/home/georgi/Music")

    def test_init(self):
        self.assertEqual(self.mc.name, "MyCrawler")
        self.mc.directory = "/home/georgi/Music"
        self.mc.mp3_files = []
        self.mc.path_to_songs = []
        self.mc.song_names = []
        self.mc.playlist = Playlist(self.mc.name)

    def test_artist_parser(self):
        self.assertEqual('Queen ', MusicCrawler.artist_parser(
            'Queen - Bohemian Rhapsody.mp3'))

    def test_title_parser(self):
        self.assertEqual(' Bohemian Rhapsody', MusicCrawler.title_parser(
            'Queen - Bohemian Rhapsody.mp3'))

    def test_generate_playlist(self):
        self.mc.generate_playlist()
        self.assertEqual(self.mc.song_names, ['Queen - Bohemian Rhapsody.mp3',
                                              'Rhapsody - Emerald Sword.mp3',
                                              "Guns N' Roses - Estranged.mp3",
                                              'Ottmar Liebert - Barcelona Nights.ogg'])

    def test_save(self):
        self.mc.generate_playlist()
        self.mc.save_generated_playlist()
        relation = session.query(MyPlaylist.id,
                                 MyPlaylist.Artist, MyPlaylist.Title,
                                 MyPlaylist.Album, MyPlaylist.rating,
                                 MyPlaylist.length, MyPlaylist.bitrate,
                                 MyPlaylist.path_to_file)
        self.assertEqual(relation[0][1], "Queen ")

    def test_load(self):
        self.mc.generate_playlist()
        self.mc.save_generated_playlist()
        self.mc.load_playlist()
        self.assertEqual(self.mc.playlist.get_first_song().artist, "Queen ")

if __name__ == '__main__':
    unittest.main()
