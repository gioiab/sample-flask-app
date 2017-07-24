#!/usr/bin/env python3
"""
This script provides facilities for creating the Flask app and running it.
"""

import os
from flask import Flask
from core.api import api
from core.models import db

from config import configs


def create_app(config='config.ProductionConfig'):
    """
    Creates the app object, infers its configuration and connects it to the database.

    :param config: a string or a object representing the default configuration
    :return: the Flask app object
    """
    app = Flask(__name__)
    # Loads the default configuration
    app.config.from_object(config)
    # Overwrites defaults with a file specified in the SAMPLE_FLASK_APP_SETTINGS environment variable
    app.config.from_envvar('SAMPLE_FLASK_APP_SETTINGS', silent=True)
    # Registers the blueprint related to the APIs
    app.register_blueprint(api)
    # Connects to the database
    db.init_app(app)
    return app


if __name__ == '__main__':
    """
    Main entry point of the program.
    """
    # Acquires the desired environment via the 'SAMPLE_FLASK_APP_ENV' environment variable
    env = os.environ.get('SAMPLE_FLASK_APP_ENV', 'default')
    # Creates the app according to the input environment
    app = create_app(config=configs[env])
    # Runs the application
    app.run()
