import os
from os.path import join, dirname
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def connect_mongo():
    client = MongoClient(os.environ.get("MONGO_URI"))
    db = client["HS"]
    return db
