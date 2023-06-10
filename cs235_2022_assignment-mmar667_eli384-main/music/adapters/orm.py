#from symbol import arith_expr
#from tkinter import N
#from colorama import Fore

from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, column
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.track import Track

metadata = MetaData()

users_table = Table(
    'users', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track', ForeignKey('tracks.id')),
    #Column('user', ForeignKey('users.id')),
    Column('track', Integer, nullable=False),
    Column('user_name', String(1024), nullable=False),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
    Column('track_url', String(255), nullable=False),
    Column('track_duration', Integer, nullable=False)
)
artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', Integer, nullable=False),
    Column('full_name', String(255), nullable=False)
)
genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', Integer, nullable=False),
    Column('name', String(255), nullable=False)
)
albums_table = Table(
    'albums', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('album_id', Integer, nullable=False),
    Column('title', String(1024), nullable=False)
)


track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

# These two tables will be deleted, for TESTING mode where these tables already exist
artists_unique_table = Table(
    'artists_unique', metadata,
    Column('artist_id', Integer, nullable=False),
    Column('full_name', String(255), nullable=False)
)

genres_unique_table = Table(
    'genres_unique', metadata,
    Column('genre_id', Integer, nullable=False),
    Column('name', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        #'_User__reviews': relationship(Review, backref='_Review__user')
    })
    mapper(Review, reviews_table, properties={
        '_Review__id': reviews_table.c.id,
        '_Review__track': relationship(Track, backref='_Track__review'),
        '_Review__track': reviews_table.c.track,
        '_Review__user_name': reviews_table.c.user_name,
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        '_Track__id': tracks_table.c.id,
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__artist': relationship(Artist, backref='_Artist__track'),
        '_Track__album': relationship(Album, backref='_Album__track'),
        '_Track__genres': relationship(Genre, secondary=track_genres_table, backref='_Genre__track'),
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration,
        #'_Track__review': relationship(Review, backref='_Review__track')
    })
    mapper(Artist, artists_table, properties={
        '_Artist__id': artists_table.c.id,
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name
    })
    mapper(Genre, genres_table, properties={
        '_Genre__id': genres_table.c.id,
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name
    })
    mapper(Album, albums_table, properties={
        '_Album__id': albums_table.c.id,
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title
    })


'''
users_table = Table(
    'users', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('user_id', Integer, nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)
reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track', ForeignKey('tracks.track_id')),
    Column('user', ForeignKey('users.id')),
    Column('username', String(1024), nullable=False),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
tracks_table = Table(
    'tracks', metadata,
    #Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', Integer, primary_key=True , nullable=False),
    Column('title', String(255), nullable=False),
    Column('artist_id', ForeignKey('artists.artist_id')),
    Column('album_id', ForeignKey('albums.album_id')),
    Column('track_url', String(255), nullable=False),
    Column('track_duration', Integer, nullable=False)
)
artists_table = Table(
    'artists', metadata,
    #Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', Integer, primary_key=True),
    Column('full_name', String(255), unique=False, nullable=False)
)
genres_table = Table(
    'genres', metadata,
    #Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', Integer, primary_key=True, nullable=False),
    Column('name', String(255), unique=False, nullable=False)
)
albums_table = Table(
    'albums', metadata, 
    #Column('id', Integer, primary_key=True, autoincrement=True),
    Column('album_id', Integer , primary_key=True, nullable=False),
    Column('title', String(1024), nullable=False)
)

track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

"""
track_artists_table = Table(
    'track_artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('artist_id', ForeignKey('artists.artist_id'))
)
"""


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, backref='_Review__user')
    })
    mapper(Review, reviews_table, properties={
        '_Review__id': reviews_table.c.id,
        '_Review__track': reviews_table.c.track,
        '_Review__username': reviews_table.c.username,
        '_Review__review': reviews_table.c.review,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(Track, tracks_table, properties={
        #'_Track__id': tracks_table.c.id,
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__album': relationship(Album, backref='_Album__track'),
        '_Track__artist': relationship(Artist, backref='_Artist__track'),
        '_Track__genres': relationship(Genre, secondary=track_genres_table, backref='_Genre__track'),
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration,
        #'_Track__review': relationship(Review, backref='_Review__track')
    })
    mapper(Artist, artists_table, properties={
        #'_Artist__id': artists_table.c.id,
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name
    })
    mapper(Genre, genres_table, properties={
        #'_Genre__id': genres_table.c.id,
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name
    })
    mapper(Album, albums_table, properties={
        #'_Album__id': albums_table.c.id,
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title
    })
'''

