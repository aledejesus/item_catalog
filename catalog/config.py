from decouple import config


class ProductionConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = \
        config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
