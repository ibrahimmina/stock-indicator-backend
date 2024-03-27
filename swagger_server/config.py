import os

class Config(object):
    LOCALHOST="http://localhost:8080/"
    DEBUG = True
    DEVELOPMENT = True
    API_KEY = os.environ.get('api_key')
    POLYGON_API_KEY = os.environ.get('polygon_api_key')
    USE_POLYGON = True
    BACK_PERIOD=30
    BACK_PERIOD_MINUTE=1
    TRADING_MINUTE_PER_DAY=590
    PERIOD_DICT = {
        'Mobile':{
            'minute': 3,
            'hour': 91,
            'day': 1825,
            'week': 3650,
            'month': 7300
        },
        'Web':{
            'minute': 3,
            'hour': 91,
            'day': 1825,
            'week': 3650,
            'month': 7300
        }
    }
    LIMIT_DICT = {
        'Mobile':{
            'minute': 125,
            'hour': 125,
            'day': 125,
            'week': 125,
            'month': 125
        },
        'Web':{
            'minute': 250,
            'hour': 250,
            'day': 250,
            'week': 250,
            'month': 250
        }
    }
class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
