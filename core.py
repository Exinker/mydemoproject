import base64
import hashlib
import hmac
import os
from typing import Optional


from settings import SECRET_KEY, PASSWORD_SALT


#
def sign_message(message: str) -> str:
    return hmac.new(
        SECRET_KEY.encode(),
        msg=message.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def assemble_cookie(message: str) -> str:
    message_signed = sign_message(message)
    message_encoded = base64.b64encode(message.encode()).decode()

    return f'{message_encoded}.{message_signed}'


def disassemble_cookie(cookie: str) -> Optional[str]:
    print(f'cookie: {cookie}')

    try:
        message_encoded, message_signed = cookie.split('.')
        message = base64.b64decode(message_encoded.encode()).decode()

        if sign_message(message) == message_signed:
            return message

    except ValueError:
        return


def verify_password(user: dict, password: str) -> bool:
    password_hash = hashlib.sha256(
        (password + PASSWORD_SALT).encode()
    ).hexdigest().lower()

    return password_hash == user['password']


def load_page(filename: str) -> str:

    filedir = './templates'
    filepath = os.path.join(filedir, filename)
    with open(filepath, 'r') as file:
        text = file.read()

    return text