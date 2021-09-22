import logging
from pathlib import Path

from flask_app.model.declarations import BaseModel


class Text2SpeechModel(BaseModel):
    def __init__(self):
        self.predictor = None

    def init_model(self, config):
        pass

    def predict(self, input_word: str) -> Path:
        """
        Translate an input word using text-to-speech model.

        Returns Path to temporary file 
        """
        # TODO: Remove placeholder
        return Path("./resources/sample/sample.mp3")

    def format_prediction(self, prediction):
        pass

    def get_visualization(self, input_image, outputs):
        pass
