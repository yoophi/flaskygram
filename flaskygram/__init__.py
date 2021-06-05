#!/usr/bin/env python
# coding: utf-8
import logging
import os
from os import path

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security

from flaskygram.config import config
from flaskygram.core.accounts.models import User, Role
from flaskygram.database import db
from flaskygram.extensions import oauth, cors, ma, debug_toolbar, mail, admin

__version__ = '0.1'

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

################################################################################
# Setup Loggers
################################################################################
logger1 = logging.getLogger('flask_oauthlib')
logger2 = logging.getLogger('oauthlib')
logger1.setLevel(logging.DEBUG)
logger2.setLevel(logging.DEBUG)
file_handler1 = logging.FileHandler('flask_oauthlib.log')
file_handler2 = logging.FileHandler('oauthlib.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s = %(message)s')
file_handler1.setFormatter(formatter)
file_handler2.setFormatter(formatter)

logger1.addHandler(file_handler1)
logger2.addHandler(file_handler2)

with open(os.path.join(os.path.dirname(__file__), 'swagger', 'swagger.yaml'), 'r') as f:
    spec_yaml = f.read()


def create_app_min(config_name='default'):
    _current_dir = path.dirname(path.abspath(__file__))
    _static_folder = path.abspath(path.join(_current_dir, 'static'))
    _template_folder = path.join(_current_dir, 'templates')
    app = Flask(__name__,
                template_folder=_template_folder,
                static_folder=_static_folder)

    app_config = config[config_name]
    app.config.from_object(app_config)
    # app_config.init_app(app)

    # app.config.from_yaml(config_name=config_name,
    #                      file_name='app.yml',
    #                      search_paths=[os.path.dirname(app.root_path)])
    # app.config.from_heroku(keys=['SQLALCHEMY_DATABASE_URI', ])

    app.config['PROJECT_ROOT'] = app.root_path
    app.config['UPLOADS_FOLDER'] = path.join(
        _static_folder,
        app.config['UPLOADS_RELATIVE_PATH']).rstrip('/')
    app.config['MEDIA_FOLDER'] = path.join(
        path.dirname(_static_folder),
        app.config['MEDIA_URL'].lstrip('/')).rstrip('/')
    app.config['MEDIA_THUMBNAIL_FOLDER'] = path.join(
        _static_folder,
        app.config['MEDIA_THUMBNAIL_URL']).rstrip('/')
    app.config['THUMBNAIL_S3_STATIC_ROOT_PARENT'] = app.root_path

    return app


def create_app(config_name='default'):
    """
    :param config_name: developtment, production or testing
    :return: flask application

    flask application generator
    """
    app = create_app_min(config_name)

    cors.init_app(app, resources={r"/v1/*": {"origins": "*"}})
    db.init_app(app)
    oauth.init_app(app)
    security.init_app(app)
    debug_toolbar.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    from flaskygram.core import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from flaskygram.core.api_1_0 import api as api_1_0_blueprint

    import flaskygram.core.accounts.api
    import flaskygram.modules.locations.api
    import flaskygram.modules.media.api
    import flaskygram.modules.posts.api
    import flaskygram.modules.tags.api

    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1')

    import flaskygram.core.accounts.admin
    import flaskygram.core.api_1_0.admin
    import flaskygram.modules.media.admin

    return app
