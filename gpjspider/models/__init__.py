# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


def get_item(self, name):
    try:
        return getattr(self, name.encode('utf8'))
    except Exception as e:
        print e, name
Base.get = Base.__getitem__ = get_item

from usedcars import UsedCar
from product import CategoryDict as BrandModel, CarSource
