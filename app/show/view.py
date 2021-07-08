#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:38 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : view.py
import logging

from flask import current_app, request

from app.show import show_bp


@show_bp.route('/', methods=['GET'])
def index():
    # celery 样例
    if current_app.config["DEBUG"] is True:
        logging.info("Hello Debug")
        # add.delay(1, 2)
        return "Hello Debug"
    else:
        logging.info("Hello Test")
        return "Hello Test"


@show_bp.route('/redis/<set_num>', methods=['GET'])
def test_redis(set_num):
    # redis样例
    redis_client = current_app.extensions['redis']
    redis_client.set('test_key', set_num)
    return "test_key is {}".format(redis_client.get('test_key'))


@show_bp.route('/add', methods=['POST'])
def add_user():
    # 增
    params = request.form
    kwargs = dict()
    kwargs["username"] = params.get("username")
    kwargs["age"] = params.get("age")
    user = TestUser.add_user(**kwargs)
    return user


@show_bp.route('/update', methods=['POST'])
def update_user():
    # 改
    params = request.form
    user_id = params.get("user_id")
    username = params.get("username")
    age = params.get("age")
    try:
        user = TestUser.get_by_id(user_id)
    except Exception as e:
        logging.exception(e)
        raise TestUserError(TestUserError.USER_NOT_FOUND, "get user failed.")
    user.update_user(username, age)
    return user.to_dict()


@show_bp.route('/delete', methods=['DELETE'])
def delete_user():
    # 删
    params = request.form
    user_id = params.get("user_id")
    try:
        user = TestUser.get_by_id(user_id)
    except Exception as e:
        logging.exception(e)
        raise TestUserError(TestUserError.USER_NOT_FOUND, "get user failed.")
    return {"user_id": user.delete_user()}
