#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 8:43 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : test_model.py

import uuid

from sqlalchemy.types import Integer, String, DateTime, Float, Boolean

from db import db


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(Integer, primary_key=True, default=uuid.uuid4().hex)
    name = db.Column(String(64), unique=True)
    describe = db.Column(String(1000))
    price = db.Column(Float, )
    addr = db.Column(String(200))
    img = db.Column(String(500))

    start_time = db.Column(DateTime)
    end_time = db.Column(DateTime)

    is_delete = db.Column(Boolean, default=False)

    create_time = db.Column(DateTime)
