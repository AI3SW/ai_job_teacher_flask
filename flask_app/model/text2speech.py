import logging
from pathlib import Path

import requests
from flask_app.commons.util import base64_to_audio
from flask_app.model.declarations import BaseModel

logger = logging.getLogger(__name__)


class Text2SpeechModel(BaseModel):
    def __init__(self):
        self.predictor = None
        self.text2speech_url = ""
        self.audio_cache_dir = None

    def init_model(self, config):
        self.text2speech_url = config['MODEL_CONFIG']['PYTHON_TTS_PREDICT_URL']
        self.audio_cache_dir = Path(config['AUDIO_PATH']).resolve()

    def predict(self, input_text: str) -> Path:
        """
        Translate an input word using text-to-speech model.

        Returns Path to audio file
        """
        file_name = '_'.join(input_text.lower().split())
        file_name = Path(file_name).with_suffix('.mp3')
        file_path: Path = self.audio_cache_dir / file_name

        # if audio file for word does not exist, send request to TTS service to get the audio
        if not file_path.exists():
            payload = {'input_text': input_text}

            try:
                response = requests.post(self.text2speech_url, json=payload)
                response_json = response.json()
                base64_audio_string = response_json['audio']
                audio_segment = base64_to_audio(base64_audio_string)
                audio_segment.export(file_path, format='mp3')

            except Exception as error:
                logger.error(error)
                raise error

        else:
            logger.info('Using cached audio file.')

        return file_path

    def format_prediction(self, prediction):
        pass

    def get_visualization(self, input_image, outputs):
        pass
