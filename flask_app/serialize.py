from pathlib import Path

from flask import current_app
from flask_marshmallow import Marshmallow
from PIL import Image

from flask_app.commons.util import image_to_base64
from flask_app.database.database import Description, Job

ma = Marshmallow()


class DescriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Description


class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        exclude = ('img_path',)

    descriptions = ma.Pluck(DescriptionSchema, "description", many=True)
    img = ma.Method("serialize_img")

    def serialize_img(self, obj: Job):
        img_path = (Path(current_app.config["ASSETS_PATH"])
                    / obj.img_path).resolve()
        img = Image.open(img_path)
        return image_to_base64(img)


job_schema = JobSchema()
job_list_schema = JobSchema(many=True)
