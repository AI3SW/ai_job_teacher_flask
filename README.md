# AI Job Teacher Flask

Repository for Flask app for AI Job Teacher

## Create Environment using Conda

```bash
$ # create conda environment
$ conda env create --file environments/environment.yml
$ conda activate ai-job-teacher-flask
```

- Installation of `psycopg2` requires installation of `libpq-dev`:

```bash
$ sudo apt-get install libpq-dev
```

- Installation of `pydub` requires installation of `ffmpeg`:

```bash
$ sudo apt-get install ffmpeg
```

## Instance Configuration

In [./instance/config.py](instance/config.py):

```python
DB_USERNAME = "postgres"
DB_PASSWORD = "PASSWORD"
DB_IP_ADDR = "<DB_IP_ADDR>"
DB_PORT = "5432"
DATABASE_NAME = "<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP_ADDR}:{DB_PORT}/{DATABASE_NAME}"
```

## Serve Flask App

### Using Flask Built-in Development Server

```bash
$ export FLASK_APP=flask_app
$ export FLASK_ENV=development
$ flask run --host=0.0.0.0 --port=5000
```

### Using Gunicorn

```bash
$ # runs on port 8000 on default
$ gunicorn -w 1 'flask_app:create_app()'
```

## Docker

### Build and Run Flask App using Docker

- Current image is only CPU compatible
- Update dockerfile, replacing `<app_name>`
- Add `instance/config` file
- Build and Run Image

```bash
$ docker build -t <app_name> -f DockerFile .
$ docker run -d --rm -p 5000:5000 <app_name>

$ # tear down container
$ docker stop <app_name>
```
