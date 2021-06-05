class Config:
    DEBUG = True
    SECRET_KEY = 'change-me'
    SQLALCHEMY_DATABASE_URI = 'postgresql://flaskygram:secret@localhost:5432/flaskygram'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_CREDENTIALS = 'admin,password'
    SECURITY_TRACKABLE = True
    SECURITY_REGISTERABLE = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MAIL_SERVER = "aspmx.l.google.com"
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', ]
    THINGY_IMAGE_RELATIVE_PATH = 'thingy_image/'
    UPLOADS_RELATIVE_PATH = 'uploads/'
    USE_S3 = True
    S3_BUCKET_NAME = ''
    S3_USE_HTTPS = False
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    MEDIA_URL = '/static/uploads/'
    MEDIA_THUMBNAIL_URL = 'cache/thumbnails/'
    THUMBNAIL_S3_STORAGE_TYPE = 's3'
    THUMBNAIL_S3_BUCKET_NAME = ''
    THUMBNAIL_S3_ACCESS_KEY_ID = ''
    THUMBNAIL_S3_ACCESS_KEY_SECRET = ''
    THUMBNAIL_S3_USE_HTTPS = False

    def init_app(self, app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SERVER_NAME = 'localhost'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    USE_S3: False
    TESTING: True


class ProductionConfig(Config):
    DEBUG = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    JSONIFY_PRETTYPRINT_REGULAR = True


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
