import os

from dotenv import load_dotenv

from conf.base import *

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

DEBUG = True
TESTING = True
SECRET_KEY = os.getenv("SECRET_KEY")

# GITHUB OAUTH
GH_CLIENT_ID = os.getenv("GH_CLIENT_ID")
GH_CLIENT_SECRET = os.getenv("GH_CLIENT_SECRET")
# MYSQL
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{server}/{database}?charset=utf8mb4".format(
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PWD"),
    server=os.getenv("MYSQL_URL"),
    database=os.getenv("MYSQL_DB"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# FrontEndHost
FRONT_HOST = "http://localhost:3000/"


class CeleryConfig:
    BROKER_URL = os.getenv("BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 * 7
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
    CELERY_IMPORTS = ("core.cookcelery.tasks", )
