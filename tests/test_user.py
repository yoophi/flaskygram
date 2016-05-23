"""
TestCase migration with Flask-Testing
"""
from flask import url_for
from sqlalchemy.exc import IntegrityError

from flaskygram.models import db, User, Relationship
from tests import BaseTestCase, load_fixtures_from_file


class UserTest(BaseTestCase):
    def test_users_self(self):
        token = self.get_oauth2_token()
        rv = self.client.get(url_for('api.users_self'), headers={'Authorization': 'Bearer ' + token})
        self.assert200(rv)


class UserModelTest(BaseTestCase):
    def test_followed_by(self):
        load_fixtures_from_file(['user_relations.json'])

        user = User.query.filter_by(email='yoophi@gmail.com').first()
        user_a = User.query.filter_by(email='a@gmail.com').first()
        user_b = User.query.filter_by(email='b@gmail.com').first()

        for u in [user, user_a, user_b]:
            self.assertIsNotNone(u)

        self.assertEqual(0, len(user.followed_by))
        self.assertEqual(0, len(user_a.follows))

        db.session.add(Relationship(user_id=user.id, followed_by_id=user_a.id))
        db.session.commit()

        self.assertEqual(1, len(user.followed_by))
        self.assertEqual(1, len(user_a.follows))

        db.session.add(Relationship(user_id=user.id, followed_by_id=user_b.id))
        db.session.commit()

        self.assertEqual(2, len(user.followed_by))
        self.assertEqual(1, len(user_a.follows))
        self.assertEqual(1, len(user_b.follows))

        db.session.add(Relationship(user_id=user.id, followed_by_id=user_a.id))
        with self.assertRaises(IntegrityError):
            db.session.commit()
