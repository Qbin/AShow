#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/8 8:43 下午
# @Author  : qinbinbin
# @email   : qinbinbin@360.cn
# @File    : test_model.py

import uuid
from datetime import date

from sqlalchemy import and_
from sqlalchemy.types import String, Date, Float, Boolean

from app.show.show_error import ShowError
from db import db


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(String(64), primary_key=True)
    name = db.Column(String(64), unique=True)
    describe = db.Column(String(1000))
    price = db.Column(Float, )
    addr = db.Column(String(200))
    img = db.Column(String(500))
    website = db.Column(String(500))

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
        self.website = kwargs.get("website")

    def create_show(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, show_id):
        show = cls.query.filter_by(id=show_id, is_delete=False).first()
        if show:
            return show
        else:
            raise ShowError(ShowError.SHOW_NOT_FOUND, "没有id为%s的show" % show_id)

    def update_show(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        db.session.commit()

    @classmethod
    def get_list(cls, page, per_page, s_time, e_time, show_name):
        s_time = date.fromisoformat(s_time)
        e_time = date.fromisoformat(e_time)

        offset = (page - 1) * per_page
        # kwargs = {
        #     'offset': offset,
        #     'per_page': per_page,
        #     'is_delete': False,
        #     's_time': s_time,
        #     'e_time': e_time,
        #     # 'user_id': g.user_id
        #
        # }
        show_list_query = cls.query.order_by(Show.start_time.desc()).filter(
            and_(
                Show.is_delete == False,
                Show.start_time <= e_time,
                Show.end_time >= s_time,
                Show.name.ilike(f'%{show_name}%')
            )
        )
        total = show_list_query.count()

        rows = [item.to_dict() for item in show_list_query.offset(offset).limit(per_page).all()]

        return {
            'total': total,
            'rows': rows
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "price": self.price,
            "addr": self.addr,
            "img": self.img,
            "website": self.website,
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
