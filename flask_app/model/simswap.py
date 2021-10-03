import logging

import requests
from flask_app.model.declarations import BaseModel

logger = logging.getLogger(__name__)


class SimSwapModel(BaseModel):
    def __init__(self):
        self.predictor = None
        self.sim_swap_url = ""

    def init_model(self, config):
        self.sim_swap_url = config['MODEL_CONFIG']['SIM_SWAP_PREDICT_URL']

    def predict(self, src_image: str, ref_img: str) -> str:
        """
        src_image: image in Base64 encoded format
        ref_img: image in Base64 encoded format

        returns output image in Base64 encoded format
        """
        payload = {
            'src_img': src_image,
            'ref_img': ref_img
        }

        try:
            response = requests.post(self.sim_swap_url, json=payload)
            response_json = response.json()
            output_img = response_json['output_img']
            return output_img
        except Exception as error:
            logger.error(error)

    def format_prediction(self, prediction):
        pass

    def get_visualization(self, input_image, outputs):
        pass
