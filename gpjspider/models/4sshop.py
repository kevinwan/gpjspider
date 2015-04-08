# -*- coding: utf-8 -*-
"""
4S店
"""
from sqlalchemy import Column, Integer, String, Float

from . import Base


class FourSShop(Base):
    """
    4S 店
    """
    __tablename__ = u'open_4s_shop'

    id = Column(Integer, primary_key=True)
    shop_name = Column(String(50), nullable=False, doc=u'名称')
    city = Column(String(32), nullable=False, doc=u'城市')
    phone = Column(String(32), nullable=True, doc=u'电话')
    address = Column(String(256), nullable=True, doc=u'详细地址')
    # 多个品牌用 ###分隔
    brands = Column(String(128), nullable=True, doc=u'经营品牌')
    longitude = Column(
        Float(128), precision=10, scale=6, asdecimal=True, doc=u'经度')
    latitude = Column(
        Float(128), precision=10, scale=6, asdecimal=True, doc=u'纬度')
    domain = Column(String(32), nullable=True, doc=u'来源网站')
    url = Column(String(500), nullable=True, default='')

    def __unicode__(self):
        return u'<4s {0} {1}>'.format(self.shop_name, self.city)
