from Playlist import Playlist
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from fnmatch import fnmatch
from Song import Song
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class MyPlaylist(Base):
    __tablename__ = "MyPlaylist"
    id = Column(Integer, primary_key=True)
    Artist = Column(String)
    Title = Column(String)
    Album = Column(String)
    rating = Column(Integer)
    length = Column(Float)
    bitrate = Column(Integer)
    path_to_file = Column(String)

engine = create_engine("sqlite:///MyPlaylist.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)


class MusicCrawler:
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        self.mp3_files = []
        self.path_to_songs = []
        self.song_names = []
        self.playlist = Playlist(name)

    @staticmethod
    def artist_parser(song_name):
        k = 0
        artist = ""
        while song_name[k] != "-":
            artist += song_name[k]
            k += 1
        return artist

    @staticmethod
    def title_parser(song_name):
        flag = False
        title = ""
        for symbol in song_name:
            if symbol == "-":
                flag = True
            if symbol == ".":
                flag = False
            if symbol != "-" and flag is True:
                title += symbol
        return title

    def generate_playlist(self):
        i = 0

        for file_name in os.listdir(self.directory):
            if fnmatch(file_name, "*.mp3") or fnmatch(file_name, "*.ogg"):
                self.song_names.append(file_name)
                self.path_to_songs.append(self.directory + "/" + file_name)
                self.mp3_files.append(
                    (MP3(self.directory + "/" + file_name, ID3=EasyID3)))

        for mp3 in self.mp3_files:
            try:
                title = mp3[0].tags["title"][0]
            except:
                title = self.title_parser(self.song_names[i])
            try:
                artist = mp3[0].tags["artist"][0]
            except:
                artist = self.artist_parser(self.song_names[i])
            try:
                album = mp3[0].tags["album"][0]
            except:
                album = "Unknown Album"
            bitrate = mp3.get("bitrate")
            length = mp3.get("length")
            self.playlist.add_song(
                Song(title, artist, album, 0, length,
                     bitrate, self.path_to_songs[i]))

            i += 1
        return self.playlist

    def save_generated_playlist(self):
        for song in self.playlist.get_all_songs():
            session.add_all([
                MyPlaylist(Artist=song.get_artist(), Title=song.get_title(),
                            Album=song.get_album(), rating=0,
                            length=song.get_length(),
                            bitrate=song.get_bitrate(),
                            path_to_file=song.get_path_to_file()),
                ])
        session.commit()

    def load_playlist(self):
        relation = session.query(MyPlaylist.id,
                                 MyPlaylist.Artist, MyPlaylist.Title,
                                 MyPlaylist.Album, MyPlaylist.rating,
                                 MyPlaylist.length, MyPlaylist.bitrate,
                                 MyPlaylist.path_to_file)
        for row in relation:
            self.playlist.add_song(Song(row[2], row[1], row[3], 0, row[5],
                                        row[6], row[7]))
        return self.playlist
