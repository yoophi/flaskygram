from flask.ext.admin import Admin
from flask.ext.config_helper import Config
from flask.ext.cors import CORS
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail
from flask.ext.marshmallow import Marshmallow
from flask.ext.oauthlib.provider import OAuth2Provider
from flask.ext.swagger_ui import SwaggerUI

admin = Admin()
config = Config()
cors = CORS()
debug_toolbar = DebugToolbarExtension()
ma = Marshmallow()
mail = Mail()
oauth = OAuth2Provider()
swagger_ui = SwaggerUI()
