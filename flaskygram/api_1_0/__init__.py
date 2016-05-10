from flask import Blueprint, url_for
from flask.ext.swagger_ui import SwaggerUI

api = Blueprint('api', __name__)


@api.before_app_first_request
def api_before_app_first_request():
    SwaggerUI().spec["securityDefinitions"]["oauth"]["authorizationUrl"] = url_for('api.user_authorize', _external=True)


from . import authentication, location, media, users, tag
