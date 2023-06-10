from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader, load_reviews, load_users

from music.domainmodel.artist import Artist

# TODO: Association between Track and Genre?

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    """
    Reads csv files and adds all objects from the csv_reader object to this repo from csv_reader object's lists to the repo's lists.
    """
    albums_file_name = str(data_path / "raw_albums_excerpt.csv")
    tracks_file_name = str(data_path / "raw_tracks_excerpt.csv") 
    reader = TrackCSVReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()
    if database_mode is False:
        for artist in reader.dataset_of_artists:
            repo.add_artist(artist)
        for genre in reader.dataset_of_genres:
            repo.add_genre(genre)
        for album in reader.dataset_of_albums:
            repo.add_album(album)
        for track in reader.dataset_of_tracks:
            repo.add_track(track)
    elif database_mode is True:
        repo.load_tracks(reader.dataset_of_tracks)
        repo.make_artists_genres_unique_table()
    users = load_users(data_path, repo)
    load_reviews(data_path, repo, users)
    