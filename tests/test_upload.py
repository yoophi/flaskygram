"""
TestCase migration with Flask-Testing
"""
from flask import url_for
from cStringIO import StringIO

from flaskygram.models import Media
from tests import BaseTestCase


class MediaTest(BaseTestCase):
    def test_upload(self):
        res = self.client.post(url_for('api.media_upload'),
                               data=dict(
                                   file=(StringIO("123456789 " * 1000), 'test.png'),
                               ),
                               headers={
                                   'Authorization': 'Bearer %s' % self.get_oauth2_token()
                               })

        self.assert200(res)
        self.assertEqual(1, Media.query.count())
