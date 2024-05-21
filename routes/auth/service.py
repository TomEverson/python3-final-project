import random
import string
from flask import current_app, Response
import resend
import uuid
import json


def generate_auth_code(username: str, email: str, password: str):
    # Generate Code
    code = ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(6))

    unique_code = str(uuid.uuid4())

    current_app.redis.set(name=unique_code, value=json.dumps({"email": email,
                                                              "password": password,
                                                              "username": username,
                                                              "code": code
                                                              }), ex=3600)

    params: resend.Emails.SendParams = {
        "sender": "Tom <tom@bluefinchfdn.org>",
        "to": [email],
        "subject": "Code For Harbour Space Social Media",
        "html": f"<strong>Code: {code}</strong>",
    }

    email = current_app.resend.Emails.send(params)

    return unique_code


def confirm_auth_code(unique_code: str, auth_code: str):
    info = json.loads(current_app.redis.get(name=unique_code))
    if (auth_code != info['code']):
        error_message = "Wrong Authentication Code"
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>'

    del info['code']
    current_app.db.users.insert_one(info)
    current_app.redis.delete(unique_code)
    return True
