from flask import Blueprint

rest_api_v1 = Blueprint('rest_api_v1', __name__)

from app.blueprints.rest_api.v1.album import resources
from app.blueprints.rest_api.v1.comment import resources
from app.blueprints.rest_api.v1.post import resources
from app.blueprints.rest_api.v1.user import resources