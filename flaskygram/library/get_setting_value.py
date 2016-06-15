from flask import current_app

from flaskygram import create_app_min
from flaskygram.database import db


def get_setting_value(key, default=None):
    try:
        return current_app.config.get(key, default)
    except RuntimeError as e:
        # logger.warning('current_app is inaccessible: %s' % e)
        pass

    try:
        app = create_app_min()
        db.init_app(app)
        with app.app_context():
            return app.config.get(key, default)
    except:
        return default

