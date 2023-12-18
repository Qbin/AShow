#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:38 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : view.py
import logging
from threading import Lock

from flask import current_app, request

from app.show import show_bp
from app.show.show_model import Show
from common.base_error import BaseError

lock = Lock()


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


@show_bp.route('/create', methods=['POST'])
def create_show():
    # 增
    params = request.json
    # print(params)

    show = Show(**params)
    show.create_show()
    return show.to_dict()


@show_bp.route('/update', methods=['PUT'])
def update_show():
    # 增
    params = request.json
    # print(params)
    show = Show.get_by_id(params.pop("show_id"))
    show.update_show(**params)
    return show.to_dict()


@show_bp.route('/get', methods=['GET'])
def get_show():
    params = request.args
    show_id = params.get('show_id', None, str)
    # print(params)
    # show_id = params.get("show_id")
    # show = Show.query.get(show_id)
    show = Show.get_by_id(show_id)
    if show:
        return show.to_dict()
    return


@show_bp.route('/list', methods=['GET'])
def get_show_list():
    params = request.args
    page = params.get('page', 1, int)
    per_page = params.get('rows', 10, int)
    s_time = params.get('s_time', "1000-01-01", str)  # 时间格式为 2020-01-02
    e_time = params.get('e_time', "9999-12-31", str)  # 时间格式为 2020-01-02
    show_name = params.get('show_name', "", str)  # 时间格式为 2020-01-02

    return Show.get_list(page, per_page, s_time, e_time, show_name)


@show_bp.route('/delete', methods=['DELETE'])
def delete_show():
    params = request.args
    show_id = params.get('show_id', None, str)
    # print(params)
    # show_id = params.get("show_id")
    show = Show.query.get(show_id)

    if show:
        show.is_delete = True

        return show.to_dict()
    return


@show_bp.route('/get_show_by_website', methods=['GET'])
def get_show_by_website():
    # 判断互斥锁是否已被持有
    if lock.locked():
        raise BaseError(BaseError.SERVER_BUSY, '服务繁忙')  # '服务繁忙'

    acquired = lock.acquire(blocking=False)

    if acquired:
        try:
            # 在这里处理请求
            params = request.args
            url = params.get('url', None, str)
            if url:
                return Show.get_show_by_website(url)
        finally:
            # 在请求处理完成后释放互斥锁
            lock.release()
    else:
        # 无法获取锁，返回自定义的响应
        BaseError(BaseError.SERVER_BUSY, '服务繁忙')
