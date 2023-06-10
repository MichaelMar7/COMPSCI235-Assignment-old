from datetime import date
from nntplib import ArticleInfo
from typing import List
from flask import session
from pytest import Session
from sqlalchemy import desc, asc

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.commit()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):
    # Add missing methods
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
    
    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
        
    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).first()
        except NoResultFound:
            pass 
        return user
    
    def add_track(self, track:Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def add_album(self, album:Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def get_track_by_id(self, id: int) -> Track:
        track = None
        try: 
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).first()
        except NoResultFound:
            pass
        return track

    def get_number_of_tracks(self):
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks
    
    def get_album_by_id(self, album_id):
        album = None
        try:
            album = self._session_cm.session.query(Album).filter(Album._Album__album_id == album_id).first()
        except NoResultFound:
            pass 
        return album
    
    def get_number_of_albums(self):
        number_of_albums = self._session_cm.session.query(Album).count()
        return number_of_albums

    def get_artist(self, artist_name):
        artist = None
        try:
            artist = self._session_cm.session.query(Artist).filter(Artist._Artist__full_name == artist_name).first()
        except NoResultFound:
            pass
        return artist
    
    def get_genre(self, genre_name):
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filter(Genre._Genre__name == genre_name).first()
        except NoResultFound:
            pass 
        return genre 
    
    def get_artist_by_id(self, id: int):
        artist = None
        try: 
            artist = self._session_cm.session.query(Artist).filter(Artist._Artist__artist_id == id).first()
        except NoResultFound:
            pass
        return artist
    
    def get_genre_by_id(self, id: int):
        genre = None
        try: 
            genre = self._session_cm.session.query(Genre).filter(Genre._Genre__genre_id == id).first()
        except NoResultFound:
            pass
        return genre
    
    def get_track_by_title(self, target_title):
        track = None
        try: 
            track = self._session_cm.session.query(Track).filter(Track._Track__title == target_title).first()
        except NoResultFound:
            pass
        return track
    
    def get_album_by_title(self, album_title):
        album = None
        try:
            album = self._session_cm.session.query(Album).filter(Album._Album__title == album_title).first()
        except NoResultFound:
            pass 
        return album

    #################
    # Track Methods #
    #################
    def get_tracks_by_id(self, id_list):
        tracks = self._session_cm.session.query(Track).filter(Track._Track__track_id.in_(id_list)).all()
        return tracks

    def get_tracks_by_album(self, target_album_name: str):
        if target_album_name is None:
            #tracks = self._session_cm.session.query(Track).all()
            #return tracks
            return list()
        else:
            album = self.get_album_by_title(target_album_name)
            tracks = self._session_cm.session.query(Track).filter(Track._Track__album == album).all()
            return tracks 

    def get_tracks_by_artist(self, target_artist_name: str):
        tracks = list()
        artist = self.get_artist(target_artist_name)
        if artist is not None:
            artist_id = artist.artist_id
            artists = self._session_cm.session.execute('SELECT id FROM artists WHERE artist_id = :artist_id', {'artist_id': artist_id}).fetchall()
            artists_list = tuple()
            for id in artists:
                if id is not None:
                    new_id = (id[0],)
                    artists_list += new_id
            tracks = self._session_cm.session.execute("SELECT * FROM tracks WHERE artist_id IN %s" % str(artists_list)).fetchall()
            return tracks
    

    def get_tracks_by_genre(self, target_genre:str):
        tracks = list()
        genre = self.get_genre(target_genre)
        if genre is not None:
            genre_id = genre.genre_id
            genres = self._session_cm.session.execute('SELECT id FROM genres WHERE genre_id = :genre_id', {'genre_id': genre_id}).fetchall()
            genres_list = tuple()
            for id in genres:
                if id is not None:
                    new_id = (id[0],)
                    genres_list += new_id
            tracks_ids = self._session_cm.session.execute("SELECT track_id FROM track_genres WHERE genre_id IN %s" % str(genres_list)).fetchall()
            tracks_ids_list = tuple()
            for id in tracks_ids:
                if id is not None:
                    new_id = (id[0],)
                    tracks_ids_list += new_id
            tracks = self._session_cm.session.execute("SELECT * FROM tracks WHERE id IN %s" % str(tracks_ids_list)).fetchall()
        return tracks
        #return list()
        """
        if target_genre is None:
            return list()
        else:
            tracks = self._session_cm.session.query(Track).filter(Track._genres == target_genre).all()
            return tracks 
        """

    def get_first_track(self):
        track = self._session_cm.session.query(Track).order_by(asc(Track._Track__track_id)).first()
        return track

    def get_last_track(self):
        track = self._session_cm.session.query(Track).order_by(desc(Track._Track__track_id)).first()
        return track

    def get_previous_track(self, track: Track):
        previous_track = self._session_cm.session.query(Track).filter(Track._Track__track_id < track.track_id).order_by(desc(Track._Track__track_id)).first()
        return previous_track

    def get_next_track(self, track: Track):
        next_track = self._session_cm.session.query(Track).filter(Track._Track__track_id > track.track_id).order_by(asc(Track._Track__track_id)).first()
        return next_track

    def track_index(self, track: Track):
        return super().track_index(track)

    #################
    # Album Methods #
    #################

    def get_albums_by_id(self, id_list):
        albums = self._session_cm.session.query(Album).filter(Album._Album__id.in_(id_list)).all()
        return albums
    
    def get_first_album(self):
        album = self._session_cm.session.query(Album).order_by(asc(Album._Album__album_id)).first()
        return album
    
    def get_last_album(self):
        album = self._session_cm.session.query(Album).order_by(desc(Album._Album__album_id)).first()
        return album

    def get_previous_album(self, album: Album):
        previous_album = self._session_cm.session.query(Album).filter(Album._Album__album_id < album.album_id).order_by(desc(Album._Album__album_id)).first()
        return previous_album

    def get_next_album(self, album: Album):
        next_album = self._session_cm.session.query(Album).filter(Album._Album__album_id > album.album_id).order_by(asc(Album._Album__album_id)).first()
        return next_album
    
    def album_index(self, album: Album):
        return super().album_index(album)

    ##################
    # Review Methods #
    ##################

    def get_reviews_for_track(self, track_id: int):
        reviews = self._session_cm.session.query(Review).filter(Review._Review__track == track_id).all()
        return reviews

    def add_review(self, review: Review):
        #super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
    
    def add_artist(self, artist:Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()

    def add_genre(self, genre:Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()
    
    def load_tracks(self, dataset_of_tracks):
        with self._session_cm as scm:
            scm.session.add_all(dataset_of_tracks)
            scm.commit()

    def make_artists_genres_unique_table(self):
        self._session_cm.session.execute("DROP TABLE IF EXISTS artists_unique")
        self._session_cm.session.execute("DROP TABLE IF EXISTS genres_unique")
        self._session_cm.session.execute("CREATE TABLE artists_unique AS SELECT DISTINCT artists.artist_id, artists.full_name FROM artists ORDER BY artists.artist_id")
        self._session_cm.session.execute("CREATE TABLE genres_unique AS SELECT DISTINCT genres.genre_id, genres.name FROM genres ORDER BY genres.genre_id")
        #self._session_cm.session.execute("SELECT DISTINCT artists.artist_id, artists.full_name INTO artists_unique IN 'music1.db' FROM artists ORDER BY artists.artist_id")
        #self._session_cm.session.execute("SELECT DISTINCT genres.genre_id, genres.name INTO genres_unique IN 'music1.db' FROM genres ORDER BY genres.genre_id")
        #self._session_cm.session.execute("INSERT INTO artists_unique (artist_id, full_name) SELECT DISTINCT artists.artist_id, artists.full_name FROM artists ORDER BY artists.artist_id")
        #self._session_cm.session.execute("INSERT INTO genres_unique (genre_id, name) SELECT DISTINCT genres.genre_id, genres.name FROM genres ORDER BY genres.genre_id")
