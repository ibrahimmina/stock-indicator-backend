import os

class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    API_KEY = os.environ.get('api_key')
    POLYGON_API_KEY = os.environ.get('polygon_api_key')
    USE_POLYGON = True
    BACK_PERIOD=30
    PERIOD_DICT = {
    'hour': 28,
    'day': 365,
    'week': 1825,
    'month': 7300
    }

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
