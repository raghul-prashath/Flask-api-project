from datetime import timedelta 

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Secret_key'
    JWT_SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///feeds.db'
    SQLALCHEMY_TRACK_MODIFICATIONS= True
    COOKIE_SECURE = False
    ACCESS_COOKIE_NAME = 'access_token_cookie'
    REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_SESSION_COOKIE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JWT_COOKIE_CSRF_PROTECT = False
        
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
