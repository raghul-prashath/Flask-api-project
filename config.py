from datetime import timedelta 

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///feeds.db'
    SQLALCHEMY_TRACK_MODIFICATIONS= True
    FLASK_ADMIN_SWATCH = 'Darkly'
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
