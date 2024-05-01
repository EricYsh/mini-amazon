# import os
# from urllib.parse import quote_plus


# class Config(object):


#     db_user = os.getenv('DB_USER', 'ubuntu')
#     db_password = os.getenv('DB_PASSWORD', 'ZhkFrwbn5uKzkdoECS2ID7wxKYgHyr')
#     db_host = os.getenv('DB_HOST', 'localhost')
#     db_port = os.getenv('DB_PORT', '5432')
#     db_name = os.getenv('DB_NAME', 'amazon')

#     SECRET_KEY = os.environ.get('SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'\
#         .format(os.environ.get('DB_USER'),
#                 quote_plus(os.environ.get('DB_PASSWORD')),
#                 os.environ.get('DB_HOST'),
#                 os.environ.get('DB_PORT'),
#                 os.environ.get('DB_NAME'))
#     SQLALCHEMY_TRACK_MODIFICATIONS = False




import os
from urllib.parse import quote_plus

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'r7oamy2kp00j1ycotuqe03t5xpmbb396_o3oqa9v83y1bvdl_e')  # provide default secret key
    DB_USER = os.environ.get('DB_USER', 'ubuntu')  # provide default user
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'ZhkFrwbn5uKzkdoECS2ID7wxKYgHyr')  # provide default password
    DB_HOST = os.environ.get('DB_HOST', 'localhost')  # provide default database host
    DB_PORT = os.environ.get('DB_PORT', '5432')  # provide default database port
    DB_NAME = os.environ.get('DB_NAME', 'amazon')  # provide default database name
#     db_user = os.getenv('DB_USER', 'ubuntu')
#     db_password = os.getenv('DB_PASSWORD', 'ZhkFrwbn5uKzkdoECS2ID7wxKYgHyr')
#     db_host = os.getenv('DB_HOST', 'localhost')
#     db_port = os.getenv('DB_PORT', '5432')
#     db_name = os.getenv('DB_NAME', 'amazon')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        quote_plus(DB_USER),
        quote_plus(DB_PASSWORD),
        quote_plus(DB_HOST),
        quote_plus(DB_PORT),
        quote_plus(DB_NAME)
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False