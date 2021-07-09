#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 8:43 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : test_model.py

import uuid

from sqlalchemy.types import String, Date, Float, Boolean

from db import db


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(String(64), primary_key=True)
    name = db.Column(String(64), unique=True)
    describe = db.Column(String(1000))
    price = db.Column(Float, )
    addr = db.Column(String(200))
    img = db.Column(String(500))

    start_time = db.Column(Date)
    end_time = db.Column(Date)

    is_delete = db.Column(Boolean, default=False)

    # create_time = db.Column(DateTime)

    def __init__(self, **kwargs):
        self.id = uuid.uuid4().hex
        self.name = kwargs.get("name")
        self.describe = kwargs.get("describe")
        self.price = kwargs.get("price")
        self.addr = kwargs.get("addr")
        self.img = kwargs.get("img")
        self.start_time = kwargs.get("start_time")
        self.end_time = kwargs.get("end_time")

    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "price": self.price,
            "addr": self.addr,
            "img": self.img,
            "start_time": self.start_time.strftime('%Y-%m-%d'),
            "end_time": self.end_time.strftime('%Y-%m-%d'),
        }

# if __name__ == '__main__':
#     from app.show.show_model import Show
# show = {
#     "name": "name",
#     "describe": "describe",
#     "price": 111,
#     "addr": "addr",
#     "img": "http://img",
# }
#     Show.query.all()
#     # Show.create(**show)
