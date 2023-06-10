from flask import session
import pytest 
from music.adapters.database_repository import SqlAlchemyRepository
from music.adapters.repository import RepositoryException
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User 

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User(4, 'Edward', 'Abc123123')
    repo.add_user(user)

    user2 = repo.get_user('edward')
    assert user2 == user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user != None

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('Someone')
    assert user is None


def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    num_of_tracks = repo.get_number_of_tracks()
    new_track_id = num_of_tracks + 1

    track = Track(new_track_id, "TEST DRIVE")

    assert track == repo.get_track_by_id(new_track_id)

def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(2)

    assert track.title == "Food"

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(9999999)

    assert track is None

def test_repository_can_get_first_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_first_track()
    assert track.title == "Food"

def test_repository_can_get_last_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_last_track()
    assert track.title == "yet to be titled"

def test_repository_can_get_tracks_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_id([2, 3, 5])
    assert len(tracks) == 3
    assert tracks[0].title == "Food"
    assert tracks[1].title == "Electric Ave"
    assert tracks[2].title == "This World"

def test_repository_does_not_retrieve_track_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_id([2, 6])
    assert len(tracks) == 1
    assert tracks[0].title == "Food"

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_id([4, 6])
    assert len(tracks) == 0

def test_repository_can_add_a_review(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    track = repo.get_track_by_id(3)
    review = Review(track, user.user_name, "Good song", 1)

    repo.add_review(review)

    assert [review] == repo.get_reviews_for_track(3)

def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews_for_track(2)) == 0

def test_repository_does_not_get_reviews_of_non_existing_track(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews_for_track(99999)) == 0

def test_repository_can_retrieve_album(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    album = repo.get_album_by_id(1)
    
    assert album.title == "AWOL - A Way Of Life"

def test_repository_does_not_retrieve_a_non_exsistent_album(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    album = repo.get_album_by_id(9999)
    assert album is None

def test_repository_can_get_first_album(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    album = repo.get_first_album()
    assert album.title == "AWOL - A Way Of Life"

def test_repository_can_get_last_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = repo.get_last_album()
    assert album.title == "Spleencoffin presents: Ladyz in Noyz"

def test_repository_can_get_albums_by_ids(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    albums = repo.get_albums_by_id([1, 4])
    assert len(albums) == 2
    assert albums[0].title == "AWOL - A Way Of Life"
    assert albums[1].title == "mp3"

def test_repository_does_not_retrieve_album_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    albums = repo.get_albums_by_id([10000, 9999])
    assert len(albums) == 0 

def test_can_retrieve_an_track_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    track = repo.get_track_by_id(20)
    review = Review(track, user.user_name, "Good song", 1)

    repo.add_review(review) 

    assert track.title == "Spiritual Level"
    assert [review] == repo.get_reviews_for_track(20)

def test_repository_does_not_add_a_review_without_a_user(session_factory): 
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(2)
    review = Review(track , "Doesnt exist", "This song is amazing", 5)
    try:
        repo.add_review(review)
    except RepositoryException:
        pass

def test_repository_can_retrieve_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album1 = repo.get_album_by_id(4)
    album2 = repo.get_album_by_title("Niris")
    
    assert album1 == album2

def test_repository_can_retrieve_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist1 = repo.get_artist_by_id(1)
    artist2 = repo.get_artist("AWOL")

    assert artist1 == artist2