from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response


from core import assemble_cookie, disassemble_cookie, verify_password, load_page
from database import users


# app
app = FastAPI()


@app.get('/')
def index_page(user_id: Optional[str] = Cookie(default=None)):
    print(f'user_id: {user_id}, {type(user_id)}')

    if not user_id:
        print('not user_id')

        response = Response(load_page('login.html'), media_type='text/html')
        response.delete_cookie(key='user_id')

        return response

    user_id = disassemble_cookie(user_id)
    if user_id:
        user = users.get(user_id)
        username = user['username']

        response = Response(f'Hello, {username}', media_type='text/html')
        return response

    else:
        response = Response(login_page)
        response.delete_cookie(key='user_id')

        return response


@app.get('/login')
def login_page():
    response = Response(load_page('login.html'), media_type='text/html')

    return response


@app.post('/login')
def login_page(email: str = Form(...), password: str = Form(...)):

    user = users.get(email, None)
    if user:
        if verify_password(user, password):
            username = user['username']

            response = Response(f'Hello, {username}', media_type='text/html')
            response.set_cookie(key='user_id', value=assemble_cookie(email))

            return response

        else:
            return Response('Password is wrong!', media_type='text/html')

    return Response(f'You are not registered!', media_type='text/html')
