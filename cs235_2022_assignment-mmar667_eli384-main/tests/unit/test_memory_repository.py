import pytest

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList
from music.adapters.repository import RepositoryException


def test_repository_add_user(in_memory_repo):
    user = User(1, "Michael", "#mmar667")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("Michael") is user

def test_repository_user_string(in_memory_repo):
    user = User(1, "Michael", "#mmar667")
    in_memory_repo.add_user(user)
    assert str(user) == "<User michael, user id = 1>"

def test_repository_user_not_in_repo(in_memory_repo):
    user = in_memory_repo.get_user("Ed")
    assert user is None


def test_repository_number_of_tracks(in_memory_repo):
    number_of_tracks = in_memory_repo.get_number_of_tracks()
    assert number_of_tracks == 2000

def test_repository_add_track_and_get_track_by_id(in_memory_repo):
    track = Track(1, "Testing123")
    in_memory_repo.add_track(track)

    assert in_memory_repo.get_track_by_id(1) is track

def test_repository_get_track_by_title(in_memory_repo):
    track = Track(1, "Testing123")
    in_memory_repo.add_track(track)
    assert in_memory_repo.get_track_by_title("Testing123") is track

def test_repository_get_existing_track(in_memory_repo):
    assert in_memory_repo.get_track_by_id(2) is in_memory_repo.get_track_by_title("Food") 

def test_repository_track_not_in_repo(in_memory_repo):
    assert in_memory_repo.get_track_by_id(1) is None

def test_repository_tracks_by_album(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_album("AWOL - A Way Of Life")
    assert len(tracks) == 4

def test_repository_tracks_by_album_not_in_repo(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_album("Fake Album")
    assert len(tracks) == 0

def test_repository_tracks_by_artist(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_artist("Nicky Cook")
    assert len(tracks) == 13

def test_repository_tracks_by_artist_not_in_repo(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_artist("Justin Bieber")
    assert len(tracks) == 0

def test_repository_tracks_by_genre(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_genre("Punk")
    assert len(tracks) == 59

def test_repository_tracks_by_genre_not_in_repo(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_genre("Dead Silence")
    assert len(tracks) == 0

def test_repository_first_track(in_memory_repo):
    track = in_memory_repo.get_first_track()
    assert in_memory_repo.get_track_by_id(2) is track

def test_repository_last_track(in_memory_repo):
    track = in_memory_repo.get_last_track()
    assert in_memory_repo.get_track_by_id(3661) is track

def test_repository_previous_track(in_memory_repo):
    track = in_memory_repo.get_track_by_id(134)
    previous_track = in_memory_repo.get_previous_track(track)
    assert in_memory_repo.get_track_by_id(48) is previous_track

def test_repository_next_track(in_memory_repo):
    track = in_memory_repo.get_track_by_id(134)
    next_track = in_memory_repo.get_next_track(track)
    assert in_memory_repo.get_track_by_id(135) is next_track


def test_repository_number_of_albums(in_memory_repo):
    number_of_albums = in_memory_repo.get_number_of_albums()
    assert number_of_albums == 427

def test_repository_add_album_and_get_album_by_id(in_memory_repo):
    album = Album(7, "Best Tracke Eva!!")
    in_memory_repo.add_album(album)
    assert in_memory_repo.get_album_by_id(7) is album

def test_repository_get_album_by_title(in_memory_repo):
    album = Album(7, "Best Tracke Eva!!")
    in_memory_repo.add_album(album)
    assert in_memory_repo.get_album_by_title("Best Tracke Eva!!") is album

def test_repository_get_existing_track(in_memory_repo):
    assert in_memory_repo.get_album_by_id(195) is in_memory_repo.get_album_by_title("Trauma") 

def test_repository_track_not_in_repo(in_memory_repo):
    assert in_memory_repo.get_album_by_id(2000) is None

def test_repository_first_album(in_memory_repo):
    album = in_memory_repo.get_first_album()
    assert in_memory_repo.get_album_by_id(1) is album

def test_repository_last_album(in_memory_repo):
    album = in_memory_repo.get_last_album()
    assert in_memory_repo.get_album_by_id(1818) is album

def test_repository_previous_album(in_memory_repo):
    album = in_memory_repo.get_album_by_id(69)
    previous_album = in_memory_repo.get_previous_album(album)
    assert in_memory_repo.get_album_by_id(68) is previous_album

def test_repository_next_album(in_memory_repo):
    album = in_memory_repo.get_album_by_id(69)
    next_album = in_memory_repo.get_next_album(album)
    assert in_memory_repo.get_album_by_id(70) is next_album


def test_repository_add_artist_and_get_artist_by_id(in_memory_repo):
    artist = Artist(2, "phillip")
    in_memory_repo.add_artist(artist)
    assert in_memory_repo.get_artist_by_id(2) is artist

def test_repository_get_artist_by_name(in_memory_repo):
    artist = Artist(2, "phillip")
    in_memory_repo.add_artist(artist)
    assert in_memory_repo.get_artist("phillip") is artist

def test_repository_get_existing_artist(in_memory_repo):
    assert in_memory_repo.get_artist_by_id(4) is in_memory_repo.get_artist("Nicky Cook") 

def test_repository_artist_not_in_repo(in_memory_repo):
    assert in_memory_repo.get_artist_by_id(3) is None

# python -m pytest tests

def test_repository_add_review(in_memory_repo):
    track_id = 2
    user = in_memory_repo.get_user('thorke')
    track = in_memory_repo.get_track_by_id(track_id)
    review = Review(track, user.user_name, "this is a review", 1)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews_for_track(track_id)

""" Comment tests <not use until reviews are added>
def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    article = in_memory_repo.get_article(2)
    comment = Comment(None, article, "Trump's onto it!", datetime.today())

    user.add_comment(comment)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 2
"""

