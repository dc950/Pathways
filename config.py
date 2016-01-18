import os
basedir = os.path.abspath(os.path.dirname(__file__))

#  SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "somethingnoonewillguesshopefully"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATHWAYS_MAIL_SUBJECT_PREFIX = '[Pathways]'
    PATHWAYS_MAIL_SENDER = 'Pathways Admin <ReflectiveEngineering@gmail.com>'
    PATHWAYS_ADMIN = os.environ.get('PATHWAYS_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ReflectiveEngineering@gmail.com'  # remove this at some point
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Group1Pathway'
    print("Running in Development mode: live at http://127.0.0.1:5000/")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'ReflectiveEngineering@gmail.com'  # remove this at some point
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Group1Pathway'
    print("Running in production mode")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
