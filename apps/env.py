import os

import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')

environ.Env.read_env(ENV_FILE_PATH)

DB_USERNAME= env('DB_USERNAME', default='temp')
DB_PASSWORD= env('DB_PASSWORD', default='temp')
DB_DATABASE= env('DB_DATABASE', default='temp')
DB_HOST= env('DB_HOST', default='127.0.0.1')
DB_PORT= env('DB_PORT', default='5432')