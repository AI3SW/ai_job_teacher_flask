import logging

from flask_app.database.database import Job
from flask_app.serialize import job_list_schema
from flask_restful import Resource

JOB_ENDPOINT = '/job'


class JobResource(Resource):
    def get(self):
        logging.info('GET %s', JOB_ENDPOINT)
        jobs = Job.query.all()
        return {"jobs": job_list_schema.dump(jobs)}
