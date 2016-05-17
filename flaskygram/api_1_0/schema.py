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
        fields = ('id', 'name', 'filesize', 'filename', 'mimetype', 'user', 'created_at')

    user = fields.Nested(UserSchema)


user_schema = UserSchema()
media_schema = MediaSchema()


