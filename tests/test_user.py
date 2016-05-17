"""
TestCase migration with Flask-Testing
"""
from flask import url_for

from tests import BaseTestCase


class UserTest(BaseTestCase):
    def test_users_self(self):
        token = self.get_oauth2_token()
        rv = self.client.get(url_for('api.users_self'), headers={'Authorization': 'Bearer ' + token})
        self.assert200(rv)
        print rv.data
