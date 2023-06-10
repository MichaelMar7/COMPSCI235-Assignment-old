import abc
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

repo_instance = None


class RepositoryException(Exception): # message (in covid app, when review not attached properly (not used))
    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        # Raises RepositoryException. But since review object is not bidirectional, I'm not sure what to do yet.
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_track_by_id(self, id: int) -> Track:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_tracks(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_album_by_id(self, album_id):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_number_of_albums(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_artist(self, artist_name):
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def get_genre(self, genre_name):
        raise NotImplementedError
    
    def get_artist_by_id(self, id: int):
        raise NotImplementedError
    
    def get_genre_by_id(self, id: int):
        raise NotImplementedError
    
    # B requirements search by methods
    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_artist(self, target_artist_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_album(self, target_album_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_genre(self, target_genre_name: str):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_first_track(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_last_track(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_previous_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def track_index(self, track: Track):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_albums_by_id(self, id_list):
        pass
    
    @abc.abstractmethod
    def get_first_album(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_album(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_previous_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next_album(self, album: Album):
        raise NotImplementedError
    
    @abc.abstractmethod
    def album_index(self, album: Album):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_reviews_for_track(self, track_id: int):
        raise NotImplementedError
    
    @abc.abstractmethod
    def load_tracks(self, dataset_of_tracks):
        raise NotImplementedError

    @abc.abstractmethod
    def make_artists_genres_unique_table(self):
        raise NotImplementedError
