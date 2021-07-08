#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:35 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : config.py

import os


# TODO 使用prophet 和 pioneer的线上环境
class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    DEBUG = False
    TESTING = False

    # Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/art_show'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(BaseConfig):
    pass


class PreConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


class LocalConfig(BaseConfig):
    pass


registered_app = [
    'app'
]

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'pre': PreConfig,
    'testing': TestingConfig,
    'local': LocalConfig
}
