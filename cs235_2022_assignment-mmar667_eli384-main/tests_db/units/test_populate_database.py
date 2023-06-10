from unicodedata import name
from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'artists_unique', 'genres', 'genres_unique','reviews', 'track_genres', 'tracks', 'users']

def test_database_populate_select_all_users(database_engine):

    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']

def test_database_populate_select_all_reviews(database_engine):

    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['username'], row['track'], row['review']))
        
        reviews = len(all_reviews)
        assert reviews == 0 

def test_database_populate_select_all_tracks(database_engine):

    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'],row['title']))

        tracks = len(all_tracks)
        assert tracks == 2000

def test_database_populate_select_all_artists(database_engine):

    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)
    
        all_artists = []
        for row in result:
            all_artists.append((row['artist_id'], row['full_name']))

        artists = len(all_artists)
        assert artists == 2000

def test_database_populate_select_all_genres(database_engine):

    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]
    
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append((row['genre_id'], row['name']))

        genres = len(all_genres)
        assert genres == 2268

def test_database_populate_select_all_albums(database_engine):

    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['album_id'], row['title']))
        
        genres = len(all_albums)
        assert genres == 427