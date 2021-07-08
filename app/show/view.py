#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:38 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : view.py
import logging

from flask import current_app, request

from app.show import show_bp
from app.show.show_model import Show


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
    show.create()
    return show.to_dict()


@show_bp.route('/get', methods=['GET'])
def get_show():
    params = request.args
    show_id = params.get('show_id', None, str)
    # print(params)
    # show_id = params.get("show_id")
    # show = Show.query.get(show_id)
    show = Show.query.filter_by(id=show_id, is_delete=False).first()
    if show:
        return show.to_dict()
    return


@show_bp.route('/list', methods=['GET'])
def get_show_list():
    params = request.args
    page = params.get('page', 1, int)
    per_page = params.get('rows', 10, int)

    offset = (page - 1) * per_page
    kwargs = {
        'offset': offset,
        'per_page': per_page,
        'is_delete': False,
        # 'user_id': g.user_id
    }
    # print(params)
    # show_id = params.get("show_id")
    # show = Show.query.filter_by(id=show_id).first()
    # return show.to_dict()
    total = Show.query.count()
    rows = [item.to_dict() for item in Show.query.all()]
    return {
        'total': total,
        'rows': rows
    }


# @show_bp.route('/delete', methods=['DELETE'])
# def delete_show():
#     params = request.args
#     show_id = params.get('show_id', None, str)
#     # print(params)
#     # show_id = params.get("show_id")
#     show = Show.query.get(show_id)
#     if show:
#         return show.to_dict()
#     return
