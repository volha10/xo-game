import os

BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = "postgresql://%(db_user)s:%(db_password)s@%(db_host)s:%(db_port)s/%(db_name)s" % {
        "db_user": os.environ['POSTGRES_USER'],
        "db_password": os.environ['POSTGRES_PASSWORD'],
        "db_name": os.environ['POSTGRES_DB'],
        "db_host": os.environ['POSTGRES_HOST'],
        "db_port": os.environ['POSTGRES_PORT']
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESTPLUS_VALIDATE = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    Testing = True
