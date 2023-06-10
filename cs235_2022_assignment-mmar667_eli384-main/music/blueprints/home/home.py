from flask import Blueprint, render_template
import music.adapters.repository as repo

import music.blueprints.utilities.utilities as utilities

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    #Takes to home page
    random_album = utilities.get_random_album(repo.repo_instance)
    random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)
    return render_template('home/home.html', random_track=utilities.get_random_track(repo.repo_instance), random_album=random_album, random_album_tracks=random_album_tracks)