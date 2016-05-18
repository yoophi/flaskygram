# -*- coding: utf8 -*-
"""
TestCase migration with Flask-Testing
"""
import json
from cStringIO import StringIO

from flask import url_for

from flaskygram.models import Post
from tests import BaseTestCase


class PostTest(BaseTestCase):
    def test_post_create(self):
        access_token = self.get_oauth2_token()
        headers = {'Authorization': 'Bearer %s' % access_token}

        # 사진을 업로드하고 and get media_id 획득
        res1 = self.client.post(url_for('api.media_upload'),
                               data=dict(
                                   file=(StringIO("123456789 " * 1000), 'test.png'),
                               ),
                               headers=headers)

        self.assert200(res1)
        media_id = json.loads(res1.data)['data']['id']

        # 획득한 media_id 이용해 게시물 등록
        res2 = self.client.post(url_for('api.post_create'),
                                data=json.dumps({
                                    'text': '첫번째 게시물',
                                    'media_id': media_id
                                }),
                                headers=headers)

        self.assert200(res2)
        self.assertEqual(1, Post.query.count())

        # 이미 사용한 media_id 이용해 게시물 등록시 실패함
        res3 = self.client.post(url_for('api.post_create'),
                                data=json.dumps({
                                    'text': '두번째 게시물',
                                    'media_id': media_id
                                }),
                                headers=headers)

        self.assert400(res3)
        self.assertEqual(1, Post.query.count())
