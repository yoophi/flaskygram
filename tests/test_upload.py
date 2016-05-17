"""
TestCase migration with Flask-Testing
"""
from flask import url_for
from cStringIO import StringIO

from flaskygram.models import Media
from tests import BaseTestCase


class UploadTest(BaseTestCase):
    def test_users_self(self):
        res = self.client.post(url_for('api.media_upload'),
                               data=dict(
                                   file=(StringIO("123456789 " * 1000), 'test.png'),
                               ),
                               headers={
                                   'Authorization': 'Bearer %s' % self.get_oauth2_token()
                               })
        print res.status_code
        print res.data
        print Media.query.all()
