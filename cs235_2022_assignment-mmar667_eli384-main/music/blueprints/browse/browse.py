from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.blueprints.utilities.utilities as utilities
import music.blueprints.browse.services as services

from music.blueprints.authentication.authentication import login_required

""""
url to escape case
"""

# Configure Blueprint
browse_blueprint = Blueprint("browse_bp", __name__)

"""
@browse_blueprint.route('/browse_tracks', methods=['GET'])
def browse_tracks_by_id():
    target_id = request.args.get("track_name")
    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_id = first_track["id"]

    return render_template("browse/tracks.html", random_track=utilities.get_random_track(repo.repo_instance), track_by_title_demo=services.get_track_by_title(repo, "Piano "))
"""
#need to add a show_comments_for_article in browse_tracks method
@browse_blueprint.route("/browse_tracks", methods=["GET", "POST"])
def browse_tracks():
    target_title = request.args.get("track_title") # http://127.0.0.1:5000/browse_tracks?track_title=<target_title>
    target_id = request.args.get("track_id") # http://127.0.0.1:5000/browse_tracks?track_id=<target_id>

    track_to_show_comments = request.args.get("view_comments_for")
    if track_to_show_comments is None:
        track_to_show_comments = -1
    else:
        track_to_show_comments = int(track_to_show_comments)

    first_track = services.get_first_track(repo.repo_instance)
    last_track = services.get_last_track(repo.repo_instance)
    if first_track is None:
        target_title = first_track.track_title
        target_id = first_track.track_id
    
    # NOTE: the target_id takes priority over target_title if both are in the URL search. If title instead takes prioity, you can swap the two if statements around
    track = first_track # default track to the first track
    if target_title is not None and services.get_track_by_title(target_title, repo) is not None:
        track = services.get_track_by_title(target_title, repo)
    if target_id is not None and services.get_track_by_id(target_id, repo) is not None:
        track = services.get_track_by_id(target_id, repo)
    
    # These are the URL links when we browse
    first_track_url = None #url_for('browse_bp.browse_tracks', track_title=first_track.title)
    last_track_url = None #url_for('browse_bp.browse_tracks', track_title=last_track.title)
    previous_track_url = None
    next_track_url = None
    add_comment_url = None

    # Only if repo tracks list is not empty, which is very unlikely except for when we do testing
    if repo.repo_instance.get_number_of_tracks() > 0:
        previous_track = services.get_previous_track(track, repo) # is None if it's on the first track
        next_track = services.get_next_track(track, repo) # is None if it's on the last track
        if previous_track is not None:
            #previous_track_url = url_for('browse_bp.browse_tracks', track_title=previous_track.title)
            #first_track_url = url_for('browse_bp.browse_tracks', track_title=first_track.title)
            previous_track_url = url_for("browse_bp.browse_tracks", track_id=previous_track.track_id)
            first_track_url = url_for("browse_bp.browse_tracks", track_id=first_track.track_id)
        if next_track is not None:
            #next_track_url = url_for('browse_bp.browse_tracks', track_title=next_track.title)
            #last_track_url = url_for('browse_bp.browse_tracks', track_title=last_track.title)
            next_track_url = url_for("browse_bp.browse_tracks", track_id=next_track.track_id)
            last_track_url = url_for("browse_bp.browse_tracks", track_id=last_track.track_id)
        view_comment_url = url_for("browse_bp.browse_tracks", view_comments_for=target_id)
        add_comment_url = url_for("browse_bp.review_track", track_id=target_id)
        """Testing
        print(first_track)
        print(last_track)
        print(previous_track)
        print(next_track)

        print(first_track_url)
        print(last_track_url)
        print(previous_track_url)
        print(next_track_url)
        """
        form = TrackSearch()
        #form2 = TrackIDSearch()
        if form.validate_on_submit():
            #print(form.input_name.data, "a")
            track_search = services.get_track_by_title(form.input_name.data, repo)
            if track_search is not None:
                return redirect(url_for("browse_bp.browse_tracks", track_id=track_search.track_id))
        """Attempted search by id, but form2 keeps linking up with form for some reason
        if form2.validate_on_submit():
            print(form2.input_name.data, "b")
            track_search = services.get_track_by_id(form2.input_name.data, repo)
            if track_search is not None:
                return redirect(url_for("browse_bp.browse_tracks", track_id=track_search.track_id))
        """

        reviews = services.get_reviews_for_track(track.track_id, repo)

        # sidebar random album
        random_album = utilities.get_random_album(repo.repo_instance)
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/tracks.html",
            page_title="Tracks",
            random_track=utilities.get_random_track(repo.repo_instance),  # random track in sidebar
            random_album=random_album,  # random album in sidebar
            random_album_tracks=random_album_tracks, # all tracks in the album from random_album
            track=track, # selected track
            first_track=first_track, # not used
            last_track=last_track, # not used
            first_track_url=first_track_url, # following are the url for the first, last, previous, and next track
            last_track_url=last_track_url,
            previous_track_url=previous_track_url,
            next_track_url=next_track_url,
            view_comment_url=view_comment_url,
            add_comment_url=add_comment_url,
            show_comments_for_track=track_to_show_comments,
            form=form,
            reviews=reviews,
            #form2=form2,
            handler_url=url_for("browse_bp.browse_tracks")
            
        )
    return redirect(url_for('home_bp.home'))

"""
Copy above method into here, but use album instead of track, and add a link in the nav for broswe album
"""
@browse_blueprint.route('/browse_albums', methods=["GET", "POST"])
def browse_albums():
    target_title = request.args.get("album_title") # http://127.0.0.1:5000/browse_albums?album_title=<target_title>
    target_id = request.args.get("album_id") # http://127.0.0.1:5000/browse_albums?album_id=<target_id>

    first_album = services.get_first_album(repo.repo_instance)
    last_album = services.get_last_album(repo.repo_instance)
    if first_album is None:
        target_title = first_album.album_title
        target_id = first_album.album_id
    
    # NOTE: the target_title takes priority over target_id if both are in the URL search. If ID instead takes prioity, you can swap the two if statements around
    album = first_album # default album to the first album
    if target_id is not None and services.get_album_by_id(target_id, repo) is not None:
        #print("a") Testing
        album = services.get_album_by_id(target_id, repo)
        #print(album)
    if target_title is not None and services.get_album_by_title(target_title, repo) is not None:
        #print("b") Testing
        album = services.get_album_by_title(target_title, repo)
        #print(album)
    #print(album)
    
    # These are the URL links when we browse
    first_album_url = None #url_for('browse_bp.browse_albums', album_title=first_album.title)
    last_album_url = None #url_for('browse_bp.browse_albums', album_title=last_album.title)
    previous_album_url = None
    next_album_url = None

    # Only if repo albums list is not empty, which is very unlikely except for when we do testing
    if repo.repo_instance.get_number_of_albums() > 0:
        previous_album = services.get_previous_album(album, repo) # is None if it's on the first album
        next_album = services.get_next_album(album, repo) # is None if it's on the last album
        #print(previous_album, next_album)
        if previous_album is not None:
            previous_album_url = url_for('browse_bp.browse_albums', album_id=previous_album.album_id)
            first_album_url = url_for('browse_bp.browse_albums', album_id=first_album.album_id)
        if next_album is not None:
            next_album_url = url_for('browse_bp.browse_albums', album_id=next_album.album_id)
            last_album_url = url_for('browse_bp.browse_albums', album_id=last_album.album_id)
        
        """Testing
        print(first_album)
        print(last_album)
        print(previous_album)
        print(next_album)

        print(first_album_url)
        print(last_album_url)
        print(previous_album_url)
        print(next_album_url)
        """
        form = AlbumSearch()
        if form.validate_on_submit():
            album_search = services.get_album_by_title(form.input_name.data, repo)
            if album_search is not None:
                return redirect(url_for("browse_bp.browse_albums", album_id=album_search.album_id))


        # sidebar random album
        random_album = utilities.get_random_album(repo.repo_instance)
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/albums.html",
            title="Albums",
            random_track=utilities.get_random_track(repo.repo_instance),  # random track in sidebar
            random_album=random_album,  # random album in sidebar
            random_album_tracks=random_album_tracks, # all tracks in the album from random_album
            album=album, # selected track
            album_tracks=repo.repo_instance.get_tracks_by_album(album.title),
            first_album=first_album, # not used
            last_album=last_album, # not used
            first_album_url=first_album_url, # following are the url for the first, last, previous, and next album
            last_album_url=last_album_url,
            previous_album_url=previous_album_url,
            next_album_url=next_album_url,
            form=form,
            handler_url=url_for("browse_bp.browse_albums")

        )
    return redirect(url_for('home_bp.home'))

"""
I'm going to complete these methods, so ask me if you're going to touch these
"""
@browse_blueprint.route('/browse_tracks_by_artist', methods=["GET", "POST"])
def browse_tracks_by_artist():
    target_artist_name = request.args.get("artist_name")
    cursor = request.args.get("cursor")
    if target_artist_name is None:
        target_artist_name = services.get_first_track(repo.repo_instance).artist.full_name

    tracks = services.get_tracks_by_artist(target_artist_name, repo)
    artist = repo.repo_instance.get_artist(target_artist_name)

    if len(tracks) > 0:
        if cursor is None or int(cursor) >= len(tracks):
            cursor = 0
        else:
            cursor = int(cursor)

        first_track_url = None
        last_track_url = None
        previous_track_url = None
        next_track_url = None

        if cursor > 0:
            previous_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist_name, cursor=cursor-1)
            first_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist_name, cursor=0)
        if cursor+1 < len(tracks):
            next_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist_name, cursor=cursor+1)
            last_track_url = url_for("browse_bp.browse_tracks_by_artist", artist_name=target_artist_name, cursor=len(tracks)-1)
        
        form = ArtistSearch()
        if form.validate_on_submit():
            return redirect(url_for("browse_bp.browse_tracks_by_artist", artist_name=form.input_name.data))

        # sidebar random album
        random_album = utilities.get_random_album(repo.repo_instance)
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/tracks_by.html",
            page_title="Tracks by Artist",
            random_track=utilities.get_random_track(repo.repo_instance),
            random_album=random_album, 
            random_album_tracks=random_album_tracks,
            track=tracks[cursor],
            browse=services.get_browse_dict("Artist", artist.full_name, artist.artist_id),
            first_track_url=first_track_url,
            last_track_url=last_track_url,
            previous_track_url=previous_track_url,
            next_track_url=next_track_url,
            form=form,
            handler_url=url_for("browse_bp.browse_tracks_by_artist")
        )
    return redirect(url_for('home_bp.home'))

@browse_blueprint.route('/browse_tracks_by_genre', methods=["GET", "POST"])
def browse_tracks_by_genre():
    target_genre_name = request.args.get("genre_name")
    cursor = request.args.get("cursor")
    if target_genre_name is None:
        target_genre_name = services.get_first_track(repo.repo_instance).genres[0].name

    tracks = services.get_tracks_by_genre(target_genre_name, repo)
    genre = repo.repo_instance.get_genre(target_genre_name)

    if len(tracks) > 0:
        if cursor is None or int(cursor) >= len(tracks):
            cursor = 0
        else:
            cursor = int(cursor)
        first_track_url = None
        last_track_url = None
        previous_track_url = None
        next_track_url = None

        if cursor > 0:
            previous_track_url = url_for("browse_bp.browse_tracks_by_genre", genre_name=target_genre_name, cursor=cursor-1)
            first_track_url = url_for("browse_bp.browse_tracks_by_genre", genre_name=target_genre_name, cursor=0)
        if cursor+1 < len(tracks):
            next_track_url = url_for("browse_bp.browse_tracks_by_genre", genre_name=target_genre_name, cursor=cursor+1)
            last_track_url = url_for("browse_bp.browse_tracks_by_genre", genre_name=target_genre_name, cursor=len(tracks)-1)
        
        form = GenreSearch()
        if form.validate_on_submit():
            return redirect(url_for("browse_bp.browse_tracks_by_genre", genre_name=form.input_name.data))

        # sidebar random album
        random_album = utilities.get_random_album(repo.repo_instance)
        random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

        return render_template(
            "browse/tracks_by.html",
            page_title="Tracks by Genre",
            random_track=utilities.get_random_track(repo.repo_instance),
            random_album=random_album, 
            random_album_tracks=random_album_tracks,
            track=tracks[cursor],
            browse=services.get_browse_dict("Genre", genre.name, genre.genre_id),
            first_track_url=first_track_url,
            last_track_url=last_track_url,
            previous_track_url=previous_track_url,
            next_track_url=next_track_url,
            form=form,
            handler_url=url_for("browse_bp.browse_tracks_by_genre")
        )
    return redirect(url_for('home_bp.home'))

@browse_blueprint.route('/review_track', methods=['GET', 'POST'])
@login_required
def review_track():
    user_name = session['user_name']
    form = CommentForm()
    if form.validate_on_submit():
        track_id = int(form.track_id.data)
        services.add_review(track_id, form.comment.data, user_name, repo.repo_instance)
        #track = services.get_track_by_id(track_id, repo)
        #return redirect(url_for("browse_bp.browse_tracks", track_title=track.title,track_id=track_id,view_comments_for=track_id))
        return redirect(url_for("browse_bp.browse_tracks",track_id=track_id,view_comments_for=track_id))
    
    if request.method == 'GET':
        if request.args.get('track_id') is None: 
            track_id = services.get_first_track(repo.repo_instance).track_id
        else:
            track_id = int(request.args.get('track_id'))
        form.track_id.data = track_id
    else:
        track_id = int(form.track_id.data)

    track = services.get_track_by_id(track_id, repo)
    # sidebar random album
    random_album = utilities.get_random_album(repo.repo_instance)
    random_album_tracks = repo.repo_instance.get_tracks_by_album(random_album.title)

    return render_template('browse/comment_on_track.html',
    random_track=utilities.get_random_track(repo.repo_instance),
    random_album=random_album, 
    random_album_tracks=random_album_tracks,
    title='Review',
    track=track,
    form=form,
    handler_url=url_for('browse_bp.review_track'))

class TrackSearch(FlaskForm):
    input_name = StringField("Track Name")
    submit = SubmitField()

class AlbumSearch(FlaskForm):
    input_name = StringField("Album Name")
    submit = SubmitField()

class ArtistSearch(FlaskForm):
    input_name = StringField("Artist Name")
    submit = SubmitField()

class GenreSearch(FlaskForm):
    input_name = StringField("Genre Name")
    submit = SubmitField()

class TrackIDSearch(FlaskForm):
    input_name = StringField("Track ID")
    submit = SubmitField()

class AlbumIDSearch(FlaskForm):
    input_name = StringField("Album ID")
    submit = SubmitField()

class ArtistIDSearch(FlaskForm):
    input_name = StringField("Artist ID")
    submit = SubmitField()

class GenreIDSearch(FlaskForm):
    input_name = StringField("Genre ID")
    submit = SubmitField()

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    track_id = HiddenField("Track id")
    submit = SubmitField('Submit')