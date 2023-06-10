from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList

class NonExistentArticleException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_review(track_id: int, review_text: str, user_name: str, repo: AbstractRepository):
    #need to check if track exists 
    #create the comment and then add it to the repo
    track = repo.get_track_by_id(track_id)
    if track is None:
        raise NonExistentArticleException
    user = repo.get_user(user_name)
    if user is None: 
        raise UnknownUserException
    #review = Review(track, user_name, review_text, 1)
    review = Review(track, user.user_name, review_text, 1)
    #print(review)
    #print(review.user_name)
    repo.add_review(review)

"""
def get_reviews_for_track(track_id: int, repo: AbstractRepository):
    track = repo.repo_instance.get_track_by_id(track_id)
    if track is None:
        raise NonExistentArticleException
    return review_to_dict(track.review_text)
"""
def get_reviews_for_track(track_id: int, repo: AbstractRepository):
    return repo.repo_instance.get_reviews_for_track(track_id)

def review_to_dict(review: Review):
    track_dict = {
        'track': review.track,
        'review_text': review.review_text,
        'rating': review.rating
    }
    return track_dict
    
def get_track_by_id(track_id: int, repo: AbstractRepository):
    track = repo.repo_instance.get_track_by_id(track_id)
    return track

def get_track_by_title(title, repo: AbstractRepository):
    track = repo.repo_instance.get_track_by_title(title)
    return track

def get_first_track(repo: AbstractRepository):
    track = repo.get_first_track()
    return track

def get_last_track(repo: AbstractRepository):
    track = repo.get_last_track()
    return track

def get_previous_track(track, repo: AbstractRepository):
    track = repo.repo_instance.get_previous_track(track)
    return track

def get_next_track(track, repo: AbstractRepository):
    track = repo.repo_instance.get_next_track(track)
    return track

def get_album(album_id: int, repo: AbstractRepository):
    album = repo.get_album(album_id)
    if album is None:
        raise NonExistentArticleException
    #return album_to_dict(album)

"""
def get_first_album(repo: AbstractRepository):
    album = repo.get_first_album()

    return track_to_dict(album)

def get_last_album(repo: AbstractRepository):
    album = repo.get_last_album()
    return track_to_dict(album)
"""

def track_to_dict(track: Track):
    article_dict = {
        "id": track.track_id,
        "title": track.title,
        "artist": track.artist,
        "album": track.album,
        "genre": track.genres,
        "track_url": track.track_url,
        #"reviews": reviews_to_dict(track.reviews)
    }
    return article_dict

def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]

def get_album_by_id(album_id: int, repo: AbstractRepository):
    album = repo.repo_instance.get_album_by_id(album_id)
    return album

def get_album_by_title(title, repo: AbstractRepository):
    album = repo.repo_instance.get_album_by_title(title)
    return album

def get_first_album(repo: AbstractRepository):
    album = repo.get_first_album()
    return album

def get_last_album(repo: AbstractRepository):
    album = repo.get_last_album()
    return album

def get_previous_album(album, repo:AbstractRepository):
    album = repo.repo_instance.get_previous_album(album)
    return album

def get_next_album(album, repo: AbstractRepository):
    album = repo.repo_instance.get_next_album(album)
    return album

def album_to_dict(album: Album):
    article_dict = {
        "id": album.album_id,
        "title": album.title,
        "release_year": album.release_year
    }
    return article_dict

def albums_to_dict(albums: Iterable[Album]):
    return [album_to_dict(album) for album in albums]

def get_tracks_by_artist(artist_name, repo: AbstractRepository):
    tracks = repo.repo_instance.get_tracks_by_artist(artist_name)
    return tracks

def get_tracks_by_genre(genre_name, repo: AbstractRepository):
    tracks = repo.repo_instance.get_tracks_by_genre(genre_name)
    return tracks

def get_browse_dict(type, title, id):
    browse_dct = {
        "type": type,
        "title": title,
        "id": id
    }
    return browse_dct
