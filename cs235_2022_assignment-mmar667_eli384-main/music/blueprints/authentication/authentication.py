from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps

import music.adapters.repository as repo
import music.blueprints.authentication.services as services
import music.blueprints.utilities.utilities as utilities

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    if form.validate_on_submit():
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your username is already taken. Please try another username.'
    random_album=utilities.get_random_album(repo.repo_instance)
    random_album_tracks=repo.repo_instance.get_tracks_by_album(random_album.title)
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register'),
        random_track=utilities.get_random_track(repo.repo_instance), 
        random_album=random_album,
        random_album_tracks=random_album_tracks)

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, contain an upper case letter, a lower case letter and a digit.'
        self.message = message
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            user_name_not_recognised = 'User name not recognised - please supply another'
        except services.AuthenticationException:
            password_does_not_match_user_name = 'Password does not match the given username. Please try again.'
    random_album=utilities.get_random_album(repo.repo_instance)
    random_album_tracks=repo.repo_instance.get_tracks_by_album(random_album.title)
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form,random_track=utilities.get_random_track(repo.repo_instance),
        random_album=random_album,
        random_album_tracks=random_album_tracks)

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view

class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')

