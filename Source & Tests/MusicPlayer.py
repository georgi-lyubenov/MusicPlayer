from MusicCrawler import MusicCrawler
from MusicCrawler import session, MyPlaylist
from Song import Song
import pygame
from random import randint
import os


class MusicPlayer():

    def __init__(self):
        self.name = None
        self.directory_path = None

    def execute(self):
        i = 1
        song_counter = 0
        while True:
            print("SHUFFLE: ON/OFF ?")
            comm = input("> ")
            if comm == "ON" or comm == "on":
                shuffle_flag = True
                break
            elif comm == "OFF" or comm == "off":
                shuffle_flag = False
                break
            else:
                print("invalid input")
        if shuffle_flag is False:
            while True:
                print("Repeat Playlist: ON/OFF ?")
                comm = input("> ")
                if comm == "ON" or comm == "on":
                    repeat_playlist_flag = True
                    break
                elif comm == "OFF" or comm == "off":
                    repeat_playlist_flag = False
                    break
                else:
                    print("invalid input")
        query = session.query(MyPlaylist.id,
                              MyPlaylist.Artist, MyPlaylist.Title,
                              MyPlaylist.Album, MyPlaylist.rating,
                              MyPlaylist.length, MyPlaylist.bitrate,
                              MyPlaylist.path_to_file)
        for song in query:
            song_counter += 1

        def play_song(index):
            pygame.init()
            pygame.mixer.music.load(query[index - 1][7])
            pygame.mixer.music.play()

        play_song(i)
        while True:
            print("type PLAY|PAUSE|UNPAUSE|STOP|PREVIOUS|NEXT|QUIT")
            command = input("> ")
            if command == "play":
                play_song(i)
            elif command == "pause":
                pygame.mixer.music.pause()
            elif command == "unpause":
                pygame.mixer.music.unpause()
            elif command == "stop":
                pygame.mixer.quit()
            elif command == "previous":
                if shuffle_flag is False:
                    i -= 1
                    play_song(i)
                elif shuffle_flag is True:
                    play_song(i)
            elif command == "next":
                if shuffle_flag is False:
                    if repeat_playlist_flag is False:
                        i += 1
                        if i <= song_counter:
                            play_song(i)
                        else:
                            print("There is no next song")
                    elif repeat_playlist_flag is True:
                        i += 1
                        if i <= song_counter:
                            play_song(i)
                        else:
                            i = 1
                            play_song(i)
                elif shuffle_flag is True:
                    while True:
                        random_number = randint(0, song_counter)
                        if random_number != i:
                            break
                    i = random_number
                    play_song(i)

            elif command == "quit":
                pygame.mixer.quit()
                print("bye!")
                break
            else:
                print("Invalid command!")

    def create_new_playlist(self, name, directory_path):
        self.name = name
        self.directory_path = directory_path
        mc = MusicCrawler(self.name, directory_path)
        self.playlist = mc.generate_playlist()
        mc.save_generated_playlist()
        print("Playlist \"{}\" was successfully created".format(self.name))

    def view_playlist(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        relation = session.query(MyPlaylist.id,
                                 MyPlaylist.Artist, MyPlaylist.Title,
                                 MyPlaylist.Album, MyPlaylist.rating,
                                 MyPlaylist.length, MyPlaylist.bitrate,
                                 MyPlaylist.path_to_file)
        for row in relation:
            print('{} - {} - {} - {}'.format(row[0], row[1], row[2], row[4]))
        print("----------------------------------")

    def prepare_song(self, path):
        head, tail = os.path.split(path)
        title = MusicCrawler.title_parser(tail)
        artist = MusicCrawler.artist_parser(tail)
        return Song(title, artist, None, 0, None, None, path)

    def playlist_options(self):
        mc = MusicCrawler(self.name, self.directory_path)
        self.playlist = mc.load_playlist()

        while True:
            print("1. ADD song to playlist")
            print("2. REMOVE song from playlist")
            print("3. RATE songs")
            print("4. REMOVE DISRATED songs")
            print("5. Exit")
            command = int(input("> "))
            if command == 1:
                song_path = input("enter song's absolute path>")
                prepared_song = self.prepare_song(song_path)
                self.playlist.add_song(prepared_song)
                session.add_all([
                    MyPlaylist(Artist=prepared_song.get_artist(),
                               Title=prepared_song.get_title(),
                               Album=prepared_song.get_album(), rating=0,
                               length=prepared_song.get_length(),
                               bitrate=prepared_song.get_bitrate(),
                               path_to_file=prepared_song.get_path_to_file()),
                ])
                session.commit()
            elif command == 2:
                self.playlist.remove_song()
            elif command == 3:
                self.playlist.rate_songs()
            elif command == 4:
                self.playlist.remove_disrated()
            elif command == 5:
                break
            else:
                print("Invalid command!")


def main():
    mp = MusicPlayer()
    print("==============================================================")
    print("Welcome to my music player!")
    # print("There are %i saved playlists" % number_of_playlists_created)
    print("Choose an option:")
    while True:
        print("1. Create new Playlist")
        print("2. View Playlist")
        print("3. Execute Playlist")
        print("4. Playlist Options")
        print("5. Exit")
        print("==============================================================")
        command = int(input("> "))
        if command == 1:
            name = input("Enter the Playlsit name> ")
            directory_path = input("Path> ")
            mp.create_new_playlist(name, directory_path)
        elif command == 2:
            # for i, song in enumerate(playlist.songs):
            #    print("{}. {}".format(i, song))
            mp.view_playlist()
        elif command == 3:
            mp.execute()
        elif command == 4:
            mp.playlist_options()
        elif command == 5:
            break
        else:
            print("Invalid command!")
if __name__ == '__main__':
    main()
