from os import environ

FLASK_APP = environ.get('FLASK_APP')
DEBUG = environ.get('DEBUG')
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
FLASK_ENV= environ.get('FLASK_ENV')
FLASK_RUN_HOST= environ.get('FLASK_RUN_HOST')
FLASK_RUN_PORT= environ.get('FLASK_RUN_PORT')