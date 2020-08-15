import os

from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions

from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class

from app import config
from app.blueprints.rest_api.utils import error_handler
from app.ext.serializer.flask_marshmallow import ma
from app.ext.database.flask_sqlalchemy import db
from app.ext.auth.flask_jwt_extended import jwt
from app.ext.log import logger

load_dotenv(find_dotenv())

photos = UploadSet('photos', IMAGES)


def create_app():
    if config.ENV_APP != 'Testing':
        logger.info(f'Starting app in {config.ENV_APP} environment')

    app = Flask(__name__)
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    for code in default_exceptions:
        app.register_error_handler(code, error_handler)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)
    configure_uploads(app, photos)
    patch_request_class(app, 5 * 1024 * 1024)

    from app.blueprints.rest_api.v1 import rest_api_v1
    app.register_blueprint(rest_api_v1, url_prefix='/api/v1')

    return app


if __name__ == '__main__':
    app.run()