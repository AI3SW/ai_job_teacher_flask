import base64
from io import BytesIO

from PIL import Image
from pydub import AudioSegment


def image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    image_bytes = base64.b64encode(buffered.getvalue())
    return image_bytes.decode("utf-8")


def base64_to_image(base64_string: str) -> Image.Image:
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_bytes))
    return image


def base64_to_audio(base64_string: str) -> AudioSegment:
    audio_bytes = base64.b64decode(base64_string)
    audio_bytes_io = BytesIO(audio_bytes)
    return AudioSegment.from_file(audio_bytes_io)
