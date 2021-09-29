from flask_marshmallow import Marshmallow

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


job_schema = JobSchema()
job_list_schema = JobSchema(many=True)
