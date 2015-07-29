# -*- coding: utf-8 -*-
"""
百度指数
"""
from sqlalchemy import Column, Integer, String, Float

from . import Base


class BaiduHot(Base):
    """
    百度指数
    """
    __tablename__ = u'baidu_hot_source'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False, doc=u'网址')
    domain = Column(String(255), nullable=False, doc=u'域名')
    keyword = Column(String(50), nullable=False, doc=u'关键词')
    score = Column(Integer, doc=u'指数')
    is_brand = Column(Integer, doc=u'是否品牌')
    the_date = Column(String(50), nullable=False, doc=u'抓取日期')

    def __unicode__(self):
        return u'<4s {0} {1}>'.format(self.keyword, self.score)
