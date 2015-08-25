class Song(object):
    MIN_RATING = 1
    MAX_RATING = 5

    def __init__(self, title, artist, album,
                 rating, length, bitrate, path_to_file):
        self.title = title
        self.artist = artist
        self.album = album
        self.rating = rating
        self.length = length
        self.bitrate = bitrate
        self.path_to_file = path_to_file

    def rate(self, rating):
        if rating in range(self.MIN_RATING, self.MAX_RATING + 1):
            self.rating = rating
        else:
            message = "Rating must be in the range [{},{}]"
            raise ValueError(message.format(self.MIN_RATING, self.MAX_RATING))

    def __str__(self):
        return "{} - {} - {}".format(self.artist, self.title, str(self.length))

    def get_path_to_file(self):
        return self.path_to_file

    def get_artist(self):
        return self.artist

    def get_title(self):
        return self.title

    def get_album(self):
        return self.album

    def get_rating(self):
        return self.rating

    def get_length(self):
        return self.length

    def get_bitrate(self):
        return self.bitrate
