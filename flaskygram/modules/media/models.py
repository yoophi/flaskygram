from flask import url_for
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from url_for_s3 import url_for_s3

from flaskygram.database import db, BaseMixin
from flaskygram.library.get_setting_value import get_setting_value


class Media(db.Model, BaseMixin):
    __tablename__ = 'media'

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='media')

    image = db.Column(db.String(255), default='')
    image_storage_type = db.Column(db.String(255), default='')
    image_storage_bucket_name = db.Column(db.String(255), default='')

    @property
    def image_url(self):
        return (self.image
                and '%s%s' % (
                    get_setting_value('UPLOADS_RELATIVE_PATH'),
                    self.image)
                or None)

    @property
    def image_url_sa(self):
        """image_url_storageaware"""
        if not self.image:
            return None

        if not (
                    self.image_storage_type
                and self.image_storage_bucket_name):
            return url_for(
                'static',
                filename=self.image_url,
                _external=True)

        if self.image_storage_type != 's3':
            raise ValueError((
                                 'Storage type "%s" is invalid, the only supported ' +
                                 'storage type (apart from default local storage) ' +
                                 'is s3.') % self.image_storage_type)

        return url_for_s3(
            'static',
            bucket_name=self.image_storage_bucket_name,
            filename=self.image_url,
            scheme='http',
        )
