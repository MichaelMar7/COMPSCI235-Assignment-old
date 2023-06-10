import music.adapters.repository as repo

import random


def get_first_track():
    for track in get_100_tracks(100, 1000):
        if track is not None:
            return track

def get_100_tracks(min, max):
    return repo.repo_instance.get_tracks_by_id([x for x in range(min, max)])

def get_track_count():
    return repo.repo_instance.get_number_of_tracks()

def get_random_track(repo):
    last_track_id = repo.get_last_track().track_id
    #last_track_id = 9999
    track = repo.get_track_by_id(random.randint(0, last_track_id))
    while track is None:
        track = repo.get_track_by_id(random.randint(0, last_track_id))
    return track

def get_random_album(repo):
    last_album_id = repo.get_last_album().album_id
    #last_album_id = 9999
    album = repo.get_album_by_id(random.randint(0, last_album_id))
    while album is None:
        album = repo.get_album_by_id(random.randint(0, last_album_id))
    return album
