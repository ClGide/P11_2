"""Some configuration for the application object used in the app defined
in server.py and for testing purposes."""

import os

from .config import SECRET_KEY

from flask import Flask


def create_app(test_config=None):
    """Creates the app, configures with the setting from config.py, sets
     the secret key and registers the blueprint from server.py"""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config["SECRET_KEY"] = SECRET_KEY

    from . import server
    app.register_blueprint(server.bp)

    return app
