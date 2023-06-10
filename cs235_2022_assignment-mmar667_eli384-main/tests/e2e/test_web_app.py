import pytest

from flask import session


def test_register(client):
    response_code = client.get("/authentication/register").status_code
    assert response_code == 200

    response = client.post(
        "/authentication/register",
        data={"user_name": "test1", "password": "Password123"}
    )
    assert response.headers["location"] == "/authentication/login"


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, contain an upper case letter, a lower case letter and a digit.'),
        ('mjackson', 'NewPassword123', b'Your username is already taken. Please try another username.')
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    response = auth.register() # user not registered yet so can't login
    response = auth.login()
    assert response.headers["Location"] == '/'

    with client:
        client.get('/')
        assert session['user_name'] == 'test1'


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Music Library' in response.data


def test_login_required_to_review(client):
    response = client.post("/review_track")
    assert response.headers["Location"] == "/authentication/login"


def test_comment(client, auth):
    auth.register()
    auth.login()

    response = client.get("/review_track?track_id=3")

    response = client.post(
        '/review_track',
        data={'comment': 'I like this track', 'track_id': 3}
    )
    assert response.headers['Location'] == "/browse_tracks?track_id=3&view_comments_for=3"


@pytest.mark.parametrize(('comment', 'messages'), (
        ('Hey', (b'Your comment is too short')),
        ('Hey Hey!', (b''))
))
def test_comment_with_invalid_input(client, auth, comment, messages):
    auth.register()
    auth.login()

    response = client.post(
        '/review_track',
        data={'comment': comment, 'track_id': 2}
    )
    for message in messages:
        assert message in response.data



def test_track_without_title_or_id(client):
    response = client.get("/browse_tracks")
    assert response.status_code == 200

    assert b"Food" in response.data
    assert b"Track ID: 2" in response.data


def test_track_with_title(client):
    response = client.get("/browse_tracks?track_title=This%20World")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_id(client):
    response = client.get("/browse_tracks?track_id=5")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_title_and_id(client):
    response = client.get("/browse_tracks?track_title=yet to be titled&track_id=5")
    assert response.status_code == 200

    assert b"This World" in response.data
    assert b"Track ID: 5" in response.data

def test_track_with_invalid_title(client):
    response = client.get("/browse_tracks?track_title=fake")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

def test_track_with_invalid_id(client):
    response = client.get("/browse_tracks?track_id=69")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page


def test_tracks_by_artist(client):
    pass

def test_tracks_by_artist_with_title(client):
    pass

def test_tracks_by_artist_with_title_and_cursor(client):
    pass

def test_tracks_by_artist_with_invalid_title(client):
    pass

def test_tracks_by_artist_with_invalid_cursor(client):
    pass

def test_tracks_by_genre(client):
    pass

def test_tracks_by_genre_with_title(client):
    pass

def test_tracks_by_genre_with_title_and_cursor(client):
    pass

def test_tracks_by_genre_with_invalid_title(client):
    pass

def test_tracks_by_genre_with_invalid_cursor(client):
    pass


def test_album_without_title_or_id(client):
    response = client.get("/browse_albums")
    assert response.status_code == 200

    assert b"AWOL - A Way Of Life" in response.data
    assert b"Album ID: 1" in response.data


def test_album_with_title(client):
    response = client.get("/browse_albums?album_title=mp3")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_id(client):
    response = client.get("/browse_albums?album_id=58")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_title_and_id(client):
    response = client.get("/browse_albums?album_title=mp3&album_id=5")
    assert response.status_code == 200

    assert b"mp3" in response.data
    assert b"Album ID: 58" in response.data

def test_album_with_invalid_title(client):
    response = client.get("/browse_tracks?album_title=fake")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

def test_album_with_invalid_id(client):
    response = client.get("/browse_tracks?album_id=9")
    assert response.status_code == 200
    #assert b"This World" in response.data # Go to a invalid page

