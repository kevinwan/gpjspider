# -*- coding: utf-8 -*-
"""
抓取过的 URL
"""


from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text

from . import Base


class RequestModel(Base):
    """
    对应 scrapy 的Request类。

    self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None
    """
    __tablename__ = u'open_requests'

    URL_CATEGORY = (
        'usedcar',  # 二手车
    )
    URL_STATUS = (
        'found',         # 被发现
        'can_download',  # 下载正常
        'can_scrape',    # 已经提取
        'need_update',   # 需要更新
        'deleted',       # 不需要再请求
    ),
    # 请求方法
    METHODS = ('GET', 'POST')

    id = Column(Integer, primary_key=True)
    url = Column(String(256), nullable=False, index=True, doc=u'URL')
    domain = Column(String(32), nullable=False, doc=u'domain')
    category = Column(Enum(URL_CATEGORY), nullable=False, doc=u'URL分类')
    updated_time = Column(
        DateTime, default=datetime.now(),
        onupdate=datetime.now, doc=u'更新请求时间'
    )
    created_time = Column(
        DateTime, default=datetime.now(),
        onupdate=datetime.now, doc=u'创建请求时间'
    )
    status = Column(Enum(URL_STATUS), default='found', doc=u'请求状态')
    method = Column(Enum(METHODS), default='GET', nullable=False, doc=u'请求方法')
    headers = Column(Text, nullable=False, doc=u'请求头')
    body = Column(Text, nullable=False, doc=u'请求体')
    cookies = Column(Text, nullable=True, doc=u'cookies')
    meta = Column(Text, nullable=True, doc=u'meta')
    encoding = Column(String(8), default='utf-8', doc=u'编码')

    UniqueConstraint('domain', 'category', 'url', name='uq_url_domain_category')

    def __unicode__(self):
        return u'<SpiderRequest {0}>'.format(self.url)
