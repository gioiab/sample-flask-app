#!/usr/bin/env python3
"""
This script provides the default configurations for the development, testing, staging
and production environments.
"""


class BaseConfig:
    DEBUG = False
    TESTING = False
    # The database URI should be provided in the following format:
    # postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@host:5432/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@localhost:5432/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@testhost:5432/dbname'
    TESTING = True


class StagingConfig(BaseConfig):
    # TODO: set the db url and the other parameters for the StagingConfig
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@staginghost:5432/dbname'


class ProductionConfig(BaseConfig):
    # TODO: set the db url and the other parameters for the ProductionConfig
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@productionhost:5432/dbname'


# Collects all the available configurations in a dictionary
configs = {'dev': DevelopmentConfig,
           'test': TestingConfig,
           'prod': ProductionConfig,
           'default': ProductionConfig}
