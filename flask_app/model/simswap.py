import logging

from flask_app.commons.util import image_to_base64
from flask_app.model.declarations import BaseModel
from PIL import Image


class SimSwapModel(BaseModel):
    def __init__(self):
        self.predictor = None

    def init_model(self, config):
        pass

    def predict(self, input_image: str) -> str:
        """
        input_image: image in Base64 encoded format

        returns output image in Base64 encoded format
        """
        # TODO: change placeholder
        placeholder = Image.open('./resources/sample/astronaut.jpg')
        encode_str = image_to_base64(placeholder)
        return encode_str

    def format_prediction(self, prediction):
        pass

    def get_visualization(self, input_image, outputs):
        pass
