import json

from flask import url_for
from flask.ext.fixtures import FixturesMixin
from flask.ext.testing import TestCase

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
