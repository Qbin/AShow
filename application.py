#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:41 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : application.py

import os
import importlib

from flask import Flask, request, g, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_log_request_id import RequestID

from config import config
from config.logger import config_logger
from common.response_handler import handle_exception, custom_response

# from common.custom_response import ProphetResponse
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from db import db


def register_logger():
    log_level = os.environ.get('LOG_LEVEL') or 'INFO'
    log_file = os.environ.get('LOG_FILE') or 'logs/app.log'
    # print("log level is {}".format(log_level))
    config_logger(
        enable_console_handler=True,
        enable_file_handler=True,
        log_level=log_level,
        log_file=log_file
    )


def register_app(app):
    for a in config.registered_app:
        module = importlib.import_module(a)
        if hasattr(module, 'register'):
            getattr(module, 'register')(app)


def get_config_object(env=None):
    if not env:
        env = os.environ.get('FLASK_ENV')
    else:
        os.environ['FLASK_ENV'] = env
    if env in config.config_map:
        return config.config_map[env]
    else:
        # set default env if not set
        env = 'production'
        return config.config_map[env]


def init_mysql(app):
    # db = SQLAlchemy(app)
    db.init_app(app)
    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)
    return app


# def create_mongo(app):
#     db = MongoEngine()
#     db.init_app(app)
#     return db


def create_redis(app):
    redis_client = FlaskRedis()
    redis_client.init_app(app)
    return app


def init_celery(celery, app):
    """
    initial celery object wraps the task execution in an application context
    """
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


def create_response_handler(app):
    @app.errorhandler(Exception)
    def handle_all_exceptions(e):
        return handle_exception(e)

    @app.after_request
    def process_response(response):
        res_json = response.get_json()
        if (res_json is not None
                and isinstance(res_json, dict) and "data" in res_json.keys() and "context" in res_json.keys()):
            return response
        if isinstance(response.get_data(), bytes):
            return custom_response(response.get_data(), response.status_code)

        return response


def create_app_by_config(conf=None, **kwargs):
    # initialize logger
    register_logger()
    # check instance path
    instance_path = os.environ.get('INSTANCE_PATH') or None
    # create and configure the app
    app = Flask("FLASK", instance_path=instance_path)
    if not conf:
        conf = get_config_object()
    app.config.from_object(conf)
    # ensure the instance folder exists
    if app.instance_path:
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
    with app.app_context():
        # register app
        register_app(app)
        init_mysql(app)
        # create_mongo(app)
        # create_redis(app)
        RequestID(app)
        # app.response_class = ProphetResponse
        create_response_handler(app)
        CORS(app, supports_credentials=True)
        # if kwargs.get('celery'):
        #     init_celery(kwargs['celery'], app)
        # app.__call__()
        # from app.user.user_error import UserError
        # @app.before_request
        # def before_request():
        #     if "login" not in request.url:
        #         try:
        #             token = request.headers['Authorization']
        #             s = Serializer(current_app.config["SECRET_KEY"])
        #             params = s.loads(token)
        #             g.user_id = params.get("user_id")
        #             g.qid = params.get("qid")
        #         except Exception:
        #             raise UserError(UserError.USER_NOT_LOGIN, "user not login")
        #
        # @app.errorhandler(UserError)
        # def handler_error(e):
        #     return UserError(UserError.USER_NOT_LOGIN, "user not login")
    return app


def create_app(env=None, **kwargs):
    conf = get_config_object(env)
    return create_app_by_config(conf, **kwargs)
