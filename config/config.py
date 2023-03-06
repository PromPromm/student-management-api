import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = 'Stores REST API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    
class TestConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'prod': ProductionConfig,
    'test': TestConfig
}
