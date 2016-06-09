#!/usr/bin/env python
# coding: utf-8
import logging
import os

from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore, Security

from flaskygram.core.accounts.models import User, Role
from flaskygram.database import db
from flaskygram.extensions import config, oauth, cors, ma, debug_toolbar, mail, swagger_ui, admin

__version__ = '0.1'

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

# Setup swagger.ui

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
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_folder)

    config.init_app(app)
    app.config.from_yaml(config_name=config_name,
                         file_name='app.yml',
                         search_paths=[os.path.dirname(app.root_path)])
    app.config.from_heroku(keys=['SQLALCHEMY_DATABASE_URI', ])

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
    swagger_ui.init_app(app, spec_yaml=spec_yaml, params={
        'OAUTH_CLIENT_ID': 'swagger',
        'OAUTH_CLIENT_SECRET': 'secret'
    })
    admin.init_app(app)

    # 업로드 경로를 절대경로로 변경
    UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER', 'data')
    if UPLOAD_FOLDER[0] != os.sep:
        UPLOAD_FOLDER = os.path.join(app.root_path, UPLOAD_FOLDER)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from flaskygram.core import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from flaskygram.core.api_1_0 import api as api_1_0_blueprint

    import flaskygram.core.accounts.api

    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1')

    import flaskygram.core.accounts.admin
    import flaskygram.core.api_1_0.admin

    return app
