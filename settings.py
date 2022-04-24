import os


#
with open('.env', 'r') as file:
    for line in file.readlines():
        key, value = line.split('=')

        os.environ[key] = value


#
SECRET_KEY = os.environ['SECRET_KEY']
PASSWORD_SALT = os.environ['PASSWORD_SALT']
