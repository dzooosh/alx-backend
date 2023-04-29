#!/usr/bin/env python3
"""
    This is a basic flask app
    with change of language, logging in with user data access
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from datetime import timezone as tzn
from pytz import timezone
import pytz.exceptions

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """
    The config settings defines:
        Language: en, fr
        Babel_default_locale - en
        Babel_default_Timezone - UTC
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


def get_user():
    """
    Returns user values against the Id specified or
    returns None if the Id is not present int the users
        data record
    """
    login_id = request.args.get('login_as', None)
    if login_id is not None:
        login_id = int(login_id)
        if login_id in users.keys():
            return users.get(login_id)
    return None


@app.before_request
def before_request():
    """
    Check if user is present using get_user() function
        and saves it in the global
    """
    user = get_user()  # user is either None or with data
    g.user = user  # assign the user value to flask global


@babel.localeselector
def get_locale():
    """
    invoked for each request to select a best match language
    works based on priority
    """
    # Locale from URL parameters
    lang = request.args.get('locale')
    if lang in app.config['LANGUAGES']:
        return lang
    # Locale from user settings
    if g.user:
        lang = g.user.get('locale')
        if lang in app.config['LANGUAGES']:
            return lang
    # Locale from request header
    loc = request.headers.get('locale', None)
    if loc in app.config['LANGUAGES']:
        return loc
    # Default locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    validate and return timezone specified
    or default to UTC
    """
    # timezone parameter in URL parameters
    tmzone = request.args.get('timezone', None)
    if tmzone:
        try:
            return timezone(tmzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # timezone from user settings
    if g.user:
        try:
            tmzone = g.user.get('timezone')
            return timezone(tmzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def home():
    """ render the template """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(debug=True)
