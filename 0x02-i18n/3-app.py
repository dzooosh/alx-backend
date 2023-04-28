#!/usr/bin/env python3
""" This is a basic flask app """
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    The config settings defines:
        Language: en, fr
        Babel_default_locale - en
        Babel_default_Timezone - UTC
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ invoked for each request to select a best match language """
    return request.accept_languages.best_match(app.config['LANGUAGES'])
    

@app.route('/')
def home():
    """ render the template """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True)
