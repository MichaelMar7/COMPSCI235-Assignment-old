import pytest

from flask import session

import music.blueprints.browse.services as services
import music.blueprints.authentication.services as services
import music.blueprints.utilities.utilities as utilities

from music.adapters.repository import RepositoryException


def test_random_track(in_memory_repo):
    random_track = utilities.get_random_track(in_memory_repo)
    assert in_memory_repo.get_track_by_id(random_track.track_id) is random_track

def test_random_album(in_memory_repo):
    random_album = utilities.get_random_album(in_memory_repo)
    assert in_memory_repo.get_album_by_id(random_album.album_id) is random_album

"""
def test_random_track_FUN(in_memory_repo): # this test has a 1 in 2000 chance to pass
    random_track = utilities.get_random_track(in_memory_repo)
    assert random_track.track_id == 1655

def test_random_album_FUN(in_memory_repo): # this test has a 1 in 2000 chance to pass
    random_album = utilities.get_random_album(in_memory_repo)
    assert random_album.album_id == 1595
"""
