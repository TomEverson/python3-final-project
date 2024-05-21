import os
from os.path import join, dirname
from dotenv import load_dotenv
from redis import Redis

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def connect_redis():
    return Redis(
        host=os.environ.get("REDIS_HOST"),
        password=os.environ.get("REDIS_PASSWORD"),
        port=os.environ.get("REDIS_PORT"),
        ssl=True
    )
