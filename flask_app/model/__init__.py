from flask_app.model.text2speech import Text2SpeechModel
from flask_app.model.simswap import SimSwapModel
import logging
import time

model_store = {}


def init_model_store(app):
    logging.info('Loading model store...')
    start_time = time.time()

    model_store['simswap'] = SimSwapModel()
    model_store['simswap'].init_model(app.config)
    logging.info("Loaded SimSwapModel")

    model_store['text2speech'] = Text2SpeechModel()
    model_store['text2speech'].init_model(app.config)
    logging.info("Loaded Text2SpeechModel")

    end_time = time.time()

    logging.info('Total time taken to load model store: %.3fs.' %
                 (end_time - start_time))
