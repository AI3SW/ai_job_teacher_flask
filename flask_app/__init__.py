import logging
from logging.config import dictConfig
from pathlib import Path

from config import LOGGING_CONFIG
from flask import Flask

dictConfig(LOGGING_CONFIG)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    # init model store
    from flask_app.model import init_model_store
    try:
        init_model_store(app)
    except Exception:
        logging.exception('Unable to init model store. Raising error.')
        raise

    # register blueprints
    from flask_app.views import blueprint
    app.register_blueprint(blueprint)

    # register db
    from flask_app.database import db
    db.init_app(app)

    # register serializer
    from flask_app.serialize import ma
    ma.init_app(app)

    # register api resources
    from flask_restful import Api

    from flask_app.resources.job import JOB_ENDPOINT, JobResource

    api = Api(app)
    api.add_resource(JobResource, JOB_ENDPOINT)

    # create resources directory if needed
    input_img_dir = Path(app.config["INPUT_IMG_PATH"])
    input_img_dir.mkdir(exist_ok=True)
    output_img_dir = Path(app.config["OUTPUT_IMG_PATH"])
    output_img_dir.mkdir(exist_ok=True)
    audio_dir = Path(app.config["AUDIO_PATH"])
    audio_dir.mkdir(exist_ok=True)

    return app
