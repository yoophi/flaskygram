import json
import os

from flask import url_for, current_app
from flask_fixtures import FixturesMixin, load_fixtures, loaders
from flask_testing import TestCase

from flaskygram import create_app, db


class BaseTestCase(TestCase, FixturesMixin):
    fixtures = ['users.json']

    def create_app(self):
        app = create_app('testing')
        FixturesMixin.init_app(app, db)

        return app

    def get_oauth2_token(self, username=None, password=None):
        if username is None:
            username = 'yoophi@gmail.com'
        if password is None:
            password = 'secret'

        query_string = {
            'grant_type': 'password',
            'client_id': 'test_client',
            'client_secret': 'secret',
            'username': username,
            'password': password,
            'scope': 'email'
        }

        rv = self.client.get(url_for("api.user_access_token"), query_string=query_string)
        return json.loads(rv.data)['access_token']

    def test_get_oauth2_token(self):
        token = self.get_oauth2_token()
        self.assertIsNotNone(token)


def load_fixtures_from_file(fixtures):
    """
    :param fixtures:
    :return:
    """
    fixtures_dirs = current_app.config['FIXTURES_DIRS']
    if not isinstance(fixtures, list):
        _fixtures = [fixtures]
    else:
        _fixtures = fixtures

    for filename in _fixtures:
        for directory in fixtures_dirs:
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                # TODO load the data into the database
                load_fixtures(db, loaders.load(filepath))
                break
        else:
            raise IOError("Error loading '{0}'. File could not be found".format(filename))
