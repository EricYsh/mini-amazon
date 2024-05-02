import os
from urllib.parse import quote_plus


class Config(object):


    db_user = os.getenv('DB_USER', 'ubuntu')
    db_password = os.getenv('DB_PASSWORD', 'ZhkFrwbn5uKzkdoECS2ID7wxKYgHyr')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'amazon')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'\
        .format(os.environ.get('DB_USER'),
                quote_plus(os.environ.get('DB_PASSWORD')),
                os.environ.get('DB_HOST'),
                os.environ.get('DB_PORT'),
                os.environ.get('DB_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

