from decouple import config


class ProductionConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = config('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = config('WTF_CSRF_SECRET_KEY')
    GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
