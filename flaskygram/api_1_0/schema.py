from marshmallow import fields

from .. import ma


class MetaSchema(ma.Schema):
    code = fields.Integer()
    message = fields.String()


class PaginationSchema(ma.Schema):
    next_url = fields.String()
    next_max_id = fields.String()


class EnvelopeSchema(ma.Schema):
    meta = fields.Nested(MetaSchema)
    data = fields.Dict()
    pagination = fields.Nested(PaginationSchema)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')


class MediaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'shortcode', 'filesize', 'mimetype', 'user', 'created_at', '_links')

    user = fields.Nested(UserSchema)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.media_file', shortcode='<shortcode>'),
    })

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'text', 'user', 'media')

    user = fields.Nested(UserSchema)
    media = fields.Nested(MediaSchema, many=True)


media_items_schema = MediaSchema(many=True)
media_schema = MediaSchema()
post_schema = PostSchema()
user_schema = UserSchema()


