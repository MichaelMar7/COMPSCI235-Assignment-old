import csv
import datetime
from pathlib import Path

from bisect import bisect, bisect_left, insort_left # when adding tracks and tracks index
from werkzeug.security import generate_password_hash

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import AbstractRepository, RepositoryException


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = list()
        self.__albums = list()
        self.__artists = list()
        self.__genres = list()
        self.__tracks_index = dict()
        self.__albums_index = dict()
        self.__artists_index = dict()
        self.__genres_index = dict()
        self.__users = list()
        self.__reviews = list()
        """
        self.__tracks and self.__albums lists are sorted by their id.
        self.__tracks_index and self.__albums_index are dictionaries that allow you to get tracks or albums depending on their id (key is id, value is object).
        other instances haven't been used yet (from what I know).
        """

    def add_track(self, track: Track):
        insort_left(self.__tracks,track)
        self.__tracks_index[track.track_id] = track
        """"
        Adds track into the self.__tracks, but uses the insort_left() method from bisect library to insert new item in sorted order.
        Also addes track into the self.__tracks_index dictionary with its id as its key, synced together.
        """
    
    def add_album(self, album: Album):
        self.__albums.append(album)
        self.__albums_index[album.album_id] = album
        """"
        Same as add_track() but uses album instead.
        """

    def add_user(self, user: User):
        self.__users.append(user)

    def add_review(self, review: Review):
        # super().add_review(review)
        self.__reviews.append(review)

    def add_artist(self, artist: Artist):
        self.__artists.append(artist)
        self.__artists_index[artist.artist_id] = artist
    
    def add_genre(self, genre: Genre):
        self.__genres.append(genre)
        self.__genres_index[genre.genre_id] = genre
    
    def get_user(self, user_name):
        """"
        next() method gets user if it's in the self.__users list via checking with a for loop, returns None if not in list.
        """
        return next((user for user in self.__users if user.user_name.lower() == user_name.lower()), None)
    
    def get_track_by_id(self, id):
        """
        (converts parameter to int if needed), uses the self.__tracks_index dictionary to get track object from it. Returns None if not in dctionary.
        """
        id = int(id)
        try:
            return self.__tracks_index[id]
        except KeyError:
            return None
     
    def get_number_of_tracks(self):
        """
        Return number of tracks in repo.
        """
        return len(self.__tracks)
    
    def get_album_by_id(self, id: int):
        """"
        Same as add_track() but uses album instead.
        """
        id = int(id)
        try:
            return self.__albums_index[id]
        except KeyError:
            return None
    
    def get_number_of_albums(self):
        """"
        Same as add_track() but uses album instead.
        """
        return len(self.__albums)
    
    def get_artist(self, artist_name):
        return next((artist for artist in self.__artists if artist.full_name.lower() == artist_name.lower()), None) 
    
    def get_genre(self, genre_name):
        return next((genre for genre in self.__genres if genre.name.lower() == genre_name.lower()), None) 
    
    def get_artist_by_id(self, id: int):
        id = int(id)
        try:
            return self.__artists_index[id]
        except KeyError:
            return None
    
    def get_genre_by_id(self, id: int):
        id = int(id)
        try:
            return self.__genres_index[id]
        except KeyError:
            return None
    
    def get_track_by_title(self, target_title):
        return next((track for track in self.__tracks if track.title.lower() == target_title.lower()), None) 
    
    def get_album_by_title(self, album_title):
        #print(album_title.strip().lower())
        #for album in self.__albums:
        #    print(album.title, album_title, album.title.lower() == album_title.strip().lower())
        return next((album for album in self.__albums if album.title.lower() == album_title.strip().lower()), None) 

    # B requirements search by methods
    """
    Tracks methods
    """
    def get_tracks_by_id(self, id_list):
        """"
        Gets a list of tracks instead from a list of ids. I haven't used this method yet.
        """
        existing_ids = [id for id in id_list if id in self.__tracks_index]
        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks
    
    def get_tracks_by_artist(self, target_artist_name: str):
        matching_tracks = list()
        matching_tracks = [track for track in self.__tracks if track is not None and target_artist_name.lower() == track.artist.full_name.lower()]
        return matching_tracks

    def get_tracks_by_album(self, target_album_name: str):
        target_album = self.get_album_by_title(target_album_name)
        matching_tracks = list()
        if target_album is not None:
            matching_tracks = [track for track in self.__tracks if track is not None and track.album == target_album]
        return matching_tracks

    def get_tracks_by_genre(self, target_genre_name: str):
        matching_tracks = list()
        matching_tracks = [track for track in self.__tracks if track is not None and target_genre_name.lower() in [genre.name.lower() for genre in track.genres]]
        return matching_tracks

    def get_first_track(self):
        if self.get_number_of_tracks() > 0:
            return self.__tracks[0]
        return None

    def get_last_track(self):
        if self.get_number_of_tracks()  > 0:
            return self.__tracks[-1]
        return None

    def get_previous_track(self, track: Track):
        try:
            index = self.track_index(track)
            for stored_track in reversed(self.__tracks[0:index]):
                if stored_track.track_id < track.track_id:
                    return stored_track
        except ValueError:
            return None

    def get_next_track(self, track: Track):
        try:
            index = self.track_index(track)
            for stored_track in self.__tracks[index + 1:len(self.__tracks)]:
                if stored_track.track_id > track.track_id:
                    return stored_track
        except ValueError:
            return None
    
    def track_index(self, track: Track):
        index = bisect_left(self.__tracks, track)
        if index != len(self.__tracks) and self.__tracks[index].track_id == track.track_id:
            return index
        raise ValueError
    
    """
    Albms methods
    """
    def get_albums_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self.__albums_index]
        albums = [self.__albums_index[id] for id in existing_ids]
        return albums

    def get_first_album(self):
        if self.get_number_of_albums() > 0:
            return self.__albums[0]
        return None

    def get_last_album(self):
        if self.get_number_of_albums() > 0:
            return self.__albums[-1]
        return None

    def get_previous_album(self, album: Album):
        try:
            index = self.album_index(album)
            for stored_album in reversed(self.__albums[0:index]):
                if stored_album.album_id < album.album_id:
                    return stored_album
        except ValueError:
            return None

    def get_next_album(self, album: Album):
        try:
            index = self.album_index(album)
            for stored_album in self.__albums[index + 1:len(self.__albums)]:
                if stored_album.album_id > album.album_id:
                    return stored_album
        except ValueError:
            return None
    
    def album_index(self, album: Album):
        index = bisect_left(self.__albums, album)
        if index != len(self.__albums) and self.__albums[index].album_id == album.album_id:
            return index
        raise ValueError
    
    def get_reviews_for_track(self, track_id: int):
        reviews = list()
        for review in self.__reviews:
            if review.track == track_id:
                reviews.append(review)
        return reviews
    
    def load_tracks(self, dataset_of_tracks):
        pass

    def make_artists_genres_unique_table(self):
        pass

#######################
#####review methods####
#######################

    



