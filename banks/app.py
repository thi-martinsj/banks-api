import logging
import sys

import json_logging
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import get_app_config
from banks.interface.views.api import api
from banks.interface.views.errors import register_error_handlers


logger = logging.getLogger("banks-api")
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(get_app_config())
    register_error_handlers(api)
    api.init_app(app)
    _set_logging(app)
    db.init_app(app)
    Migrate(app, db)

    return app


def _set_logging(app: Flask):
    json_logging.init_flask(enable_json=True)
    json_logging.init_request_instrument(app)

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    @app.before_request
    def log_request():
        logger.info(
            "Request received",
            extra={
                "props": {
                    "path": request.path,
                    "method": request.method,
                    "payload": request.json if request.mimetype == "application/json" else None
                }
            }
        )

    @app.after_request
    def log_response(response):
        logger.info(
            "Request response",
            extra={
                "props": {
                    "path": request.path,
                    "method": request.method,
                    "status": response.status_code,
                    "body": response.json
                }
            },
        )

        return response
