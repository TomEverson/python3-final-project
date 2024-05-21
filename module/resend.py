import resend
import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def connect_resend():
    resend.api_key = os.environ.get("RESEND_API_KEY")
    return resend
