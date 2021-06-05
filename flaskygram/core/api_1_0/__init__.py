from flask import Blueprint, url_for

api = Blueprint('api', __name__)



from . import authentication  # NOQA
