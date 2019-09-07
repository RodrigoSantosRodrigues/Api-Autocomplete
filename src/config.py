# -*- coding: utf-8 -*-
# /src/config.py
"""
                          Api Auto complete
    ------------------------------------------------------------------------
                        Flask Environment Configuration
    ------------------------------------------------------------------------
    
    URLs: https://flask.palletsprojects.com/en/1.1.x/


"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("../.env"))

POSTGRES_DEVELOPER = {
    'user': os.getenv('DB_USER'),
    'pw': os.getenv('DB_PW'),
    'db': os.getenv('DB_DEVELOPER'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT') or '5432',
}
POSTGRES_TESTS = {
    'user': os.getenv('DB_USER'),
    'pw': os.getenv('DB_PW'),
    'db': os.getenv('DB_TEST'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT') or '5432',
}
POSTGRES_PRODUCTION = {
    'user': os.getenv('DB_USER'),
    'pw': os.getenv('DB_PW'),
    'db': os.getenv('DB_PRODUCTION'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT') or '5432',
}

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY= os.getenv('APP_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_DEVELOPER

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY= os.getenv('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_PRODUCTION
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    SECRET_KEY= os.getenv('APP_SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_TESTS
    SQLALCHEMY_TRACK_MODIFICATIONS=False

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
