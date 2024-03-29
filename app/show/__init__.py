#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:39 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : __init__.py


import types
from flask import Blueprint
from common.service_decorator import route

show_bp = Blueprint("show", __name__, url_prefix="/show")
show_bp.route = types.MethodType(route, show_bp)
