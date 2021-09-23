import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, current_app, render_template, request, send_file

from flask_app.commons.util import base64_to_image
from flask_app.database import db
from flask_app.database.database import InputImg, OutputImg, Session, User
from flask_app.model import model_store, simswap, text2speech

blueprint = Blueprint('blueprint', __name__)


@blueprint.route('/')
def index():
    logging.info("GET /")
    return render_template('index.html')


@blueprint.route('/image', methods=['POST'])
def predict():
    logging.info("POST /image")
    req: dict = request.get_json()

    # TODO: serialize endpoint input in flask_app/serialize.py
    expected_keys = {'user_id', 'img', 'job_id'}
    if req.keys() != expected_keys:
        missing_keys = expected_keys - req.keys()
        error_msg = f"keys missing from request {missing_keys}"
        logging.exception(error_msg)
        return {'error': error_msg}

    # TODO: better exception handling
    try:
        start_time = time.time()

        # get inputs
        user_id = req.get('user_id')
        img = req.get('img')
        job_id = req.get('job_id')

        # TODO: check that job_id is in db
        # TODO: offload image save to a background process

        # process input image
        input_pil_img = base64_to_image(img)
        input_file_path = Path(current_app.config['INPUT_IMG_PATH']) \
            / f'{uuid.uuid4()}.png'

        input_pil_img.save(input_file_path)
        input_img = InputImg(file_path=str(input_file_path.resolve()))

        # process output image
        model: simswap.SimSwapModel = model_store['simswap']
        output_base64_img: str = model.predict(img)
        output_pil_img = base64_to_image(output_base64_img)
        output_file_path = Path(current_app.config['OUTPUT_IMG_PATH']) \
            / f'{uuid.uuid4()}.png'
        output_pil_img.save(output_file_path)
        output_img = OutputImg(file_path=str(output_file_path.resolve()))

        # commit input image, output image and user before processing session
        db.session.add(input_img)
        db.session.add(output_img)
        user = User.query.get(user_id)
        if not user:
            user = User(id=user_id)
            db.session.add(user)
        db.session.commit()

        # process session
        session = Session(user_id=user.id, job_id=job_id,
                          input_img_id=input_img.id,
                          output_img_id=output_img.id,
                          start_time=datetime.fromtimestamp(start_time, timezone.utc))
        db.session.add(session)
        db.session.commit()

        response = {'output_img': output_base64_img}

        end_time = time.time()
        logging.info('Total processing time: %.3fs.' % (end_time - start_time))

        return response

    except Exception as error:
        logging.exception(error)
        return {'error': 'Error in prediction'}


@blueprint.route('/audio', methods=['GET'])
def get_audio():
    logging.info('GET /audio')

    input_string = request.args.get('input', '')
    if not input_string:
        error_msg = "No input_string detected"
        logging.exception(error_msg)
        return {'error': error_msg}

    model: text2speech.Text2SpeechModel = model_store['text2speech']
    output_file_path = model.predict(input_string)

    try:
        return send_file(str(output_file_path.resolve()))
    except FileNotFoundError:
        error_msg = f"File not found at {output_file_path}"
        logging.exception(error_msg)
        return {'error': error_msg}
