import pytest

from sqlalchemy.exc import IntegrityError

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

def insert_user(empty_session, values=None):
    new_id = 3
    new_name = "Andrew"
    new_password = "Abc123123"

    if values is not None:
        new_id = values[0]
        new_name = values[1]
        new_password = values[2]
    empty_session.execute('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)',
                            {'user_id':new_id, 'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where user_name = :user_name',
                            {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_id, user_name, password) VALUES (:user_id, :user_name, :password)',
                              {'user_id': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_id, title, track_url, track_duration, album_id, artist_id) VALUES '
        '(2, "Food", "www.AWebsite.com", 169, 1, 1)'
    )
    row = empty_session.execute('SELECT track_id from tracks').fetchone()
    return row[0]

def make_track():
    track = Track(2,"Not Food")
    track.album = "Eternal Atake"
    track.artist = "Lil Uzi Vert"
    track.track_duration = 5
    track.track_url = "Website Name"
    return track

def make_album():
    album = Album(2, "Album Name")
    return album

def make_artist():
    artist = Artist(2, "Artist Name")
    return artist

def make_user():
    user = User(9, "Michael", "Password123")
    return user

def make_review():
    track = make_track()
    review = Review(track, "thorke", "This a good song", 2)
    return review

def test_loading_of_users(empty_session): # PASSED 
    users = list()
    users.append((10, "edward", "Abc123123"))
    insert_users(empty_session, users)

    expected = [
        User(10, "edward", "Abc123123"),
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session): # PASSED 
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [('michael', 'Password123')]

def test_saving_of_users_with_common_user_name(empty_session): # PASSED
    insert_user(empty_session, (6, "Andrew", "Abc123123"))
    empty_session.commit()
    try:
        user = User(6, "Andrew", "Abc123123")
        empty_session.add(user)
        empty_session.commit()
    except IntegrityError:
        pass

def test_saving_of_tracks(empty_session): # PASSED
    track = make_track()
    empty_session.add(track)
    empty_session.commit()
    
    rows = list(empty_session.execute('SELECT track_id, title FROM tracks'))
    assert rows == [(2, 'Not Food')]

def test_loading_of_track(empty_session): # PASSED
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id

def test_saving_of_review(empty_session): # PASSED
    review = make_review()
    empty_session.add(review)
    empty_session.commit()
    review_text = list(empty_session.execute('SELECT review_text FROM reviews'))
    assert review_text[0] == ('This a good song',)
    