import os

from flask import Flask, redirect
from flask.ext.admin import Admin
from flask.ext.config_helper import Config

from ..models import db

admin = Admin()
config = Config()


def create_app(config_name):
    app = Flask(__name__)
    config.init_app(app)
    app.config.from_yaml(config_name=config_name,
                         file_name='app.yml',
                         search_paths=[os.path.dirname(os.path.dirname(app.root_path)), ])
    app.config.from_heroku(keys=['SQLALCHEMY_DATABASE_URI', ])

    db.init_app(app)
    admin.init_app(app)

    @app.route('/')
    def index():
        return redirect('/admin')

    from . import views

    return app
