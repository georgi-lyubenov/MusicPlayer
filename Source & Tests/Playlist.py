from Song import Song
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import update

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


class Playlist(Song):
    MIN_BITRATE = 64

    def __init__(self, name):
        self.name = name
        self.songs = []

    def get_first_song(self):
        return self.songs[0]

    def get_all_songs(self):
        return self.songs

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        relation = session.query(MyPlaylist.id,
                                 MyPlaylist.Artist, MyPlaylist.Title,
                                 MyPlaylist.Album, MyPlaylist.rating,
                                 MyPlaylist.length, MyPlaylist.bitrate,
                                 MyPlaylist.path_to_file)
        for row in relation:
            print('{} - {} - {} - {}'.format(row[0], row[1], row[2], row[4]))
        print("----------------------------------")
        song_id = int(input("enter song id> "))
        for row in relation:
            for song in self.songs:
                if row[2] == song.get_title():
                    self.songs.remove(song)
        session.query(MyPlaylist).\
            filter(MyPlaylist.id == song_id).delete()
        session.commit()

    def rate_songs(self):
        print("Rate each song with number from 1 to 5")
        for song in self.songs:
            new_rating = int(input("Rate song \"{}-{}\": "
                             .format(song.get_artist(), song.get_title())))
            song.rate(new_rating)
            session.query(MyPlaylist).\
                filter(MyPlaylist.Title == song.get_title()).\
                update({"rating": (new_rating)})
        session.commit()

    def remove_disrated(self):
        minimal_rating = int(input("choose the minimal rating: "))
        for song in self.songs:
            if song.rating < minimal_rating:
                self.songs.remove(song)
                # self.totalLength -= song.length
        session.query(MyPlaylist).\
            filter(MyPlaylist.rating < minimal_rating).delete()
        session.commit()

    def __str__(self):
        result = ""
        for i in range(len(self.songs)):
            result += str(self.songs[i])
            if i != len(self.songs) - 1:
                result += "\n"
        return result


