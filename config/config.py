import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
url = config('DATABASE_URL')
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql://', 1)

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = 'Stores REST API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'topsecret')
    API_SPEC_OPTIONS = {
        'security':[{"bearerAuth": []}],
        'components':{
            "securitySchemes":
                {
                    "bearerAuth": {
                        "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize **"
                    }
                }
        }
    }

class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    
class TestConfig(Config):
    pass

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)

config_dict = {
    'dev': DevConfig,
    'prod': ProductionConfig,
    'test': TestConfig
}
