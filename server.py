#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/7 7:42 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : server.py
import os

from application import create_app

app = create_app(os.getenv('FLASK_ENV') or 'development')
