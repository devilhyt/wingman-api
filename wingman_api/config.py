from flask import Flask
import datetime

WINGMAN_ROOT = 'C:/Users/DevilHYT/Desktop/github/wingman-api'
WINGMAN_DATA_DIR_NAME = 'wingman_data'
WINGMAN_PRJ_DIR_NAME = 'wingman_projects'

WINGMAN_DATA_DIR = f'{WINGMAN_ROOT}/{WINGMAN_DATA_DIR_NAME}'
WINGMAN_PRJ_DIR = f'{WINGMAN_DATA_DIR}/{WINGMAN_PRJ_DIR_NAME}'

OUTPUT_DIR_NAME = 'output'

INTENTS_FILE_NAME = 'intents.json'
ACTIONS_FILE_NAME = 'actions.json'
ENTITIES_FILE_NAME = 'entities.json'
SLOTS_FILE_NAME = 'slots.json'
STORIES_FILE_NAME = 'stories.json'
RULES_FILE_NAME = 'rules.json'
TOKENS_FILE_NAME = 'tokens.json'
MODELS_FILE_NAME = 'model.tar.gz'
JIEBA_DICT_NAME = 'userdict.txt'
TRAINING_DATA_FILE_NAME = 'training_data.yml'
ACTIONS_PY_NAME = 'action.py'

SERVER_URL = 'http://localhost:5000'
RASA_URL = 'http://localhost:5005'

class DevelopmentConfig(object):
    """Flask Config"""

    SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{WINGMAN_DATA_DIR}/wingman.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'b0cf91e59567ee4951077964046cb574bddc5d9e461613d9c328f7089d448269'
    JWT_TOKEN_LOCATION = ['headers', 'cookies', 'query_string', 'json']
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=12)
    
    @classmethod
    def init_app(cls, app:Flask):
        app.json.sort_keys = False
