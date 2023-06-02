from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

BUILD_VERSION = environ.get("BUILD_VERSION")
METRICS_PATH = environ.get("METRICS_PATH")
NAME = environ.get("NAME")
HTTPPORT = environ.get("HTTPPORT")
HOST = environ.get("HOST")
CB_USERNAME = environ.get("CB_USERNAME")
CB_PASSWORD = environ.get("CB_PASSWORD")
CB_BUCKET_NAME = environ.get("CB_BUCKET_NAME")
CB_CLIENT_COLLECTION = environ.get("CB_CLIENT_COLLECTION")
CB_BLACKLIST_COLLECTION = environ.get("CB_BLACKLIST_COLLECTION")
CB_CLUSTER = environ.get("CB_CLUSTER")
