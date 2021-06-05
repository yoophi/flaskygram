from flask_admin import Admin
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_oauthlib.provider import OAuth2Provider

admin = Admin()
cors = CORS()
debug_toolbar = DebugToolbarExtension()
ma = Marshmallow()
mail = Mail()
oauth = OAuth2Provider()
