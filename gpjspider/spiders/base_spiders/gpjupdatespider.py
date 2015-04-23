# -*- coding: utf-8 -*-
"""
公平价更新爬虫
"""
import pickle
from scrapy import log
from scrapy.http import Request
from gpjspider.utils import get_mysql_connect
from gpjspider.models.requests import RequestModel
from gpjspider.models.product import CarSource
from gpjspider.utils.path import import_item
from gpjspider.utils.path import import_update_rule
from .gpjbasespider import GPJBaseSpider


class GPJUpdateSpider(GPJBaseSpider):
    def __init__(self, rule_name, checker_name=None, *args, **kwargs):
        if import_update_rule(rule_name):
            rule_name = 'update.' + rule_name
        super(GPJUpdateSpider, self).__init__(rule_name)
        self.checker.check()
        self.Session = get_mysql_connect()

    def start_requests(self):
        """
        start_urls_category
        """
        if 'start_urls_category' not in self.website_rule:
            self.log(u'无start_urls_category规则', log.ERROR)
            yield None
        category = self.website_rule['start_urls_category']
        self.log(u'开始爬取{0}的{1}分类 URL'.format(self.domain, category), log.INFO)
        session = self.Session()
        q = session.query(RequestModel)
        q = q.filter(RequestModel.domain == self.domain)
        q = q.filter(RequestModel.category == category)
        q = q.filter(RequestModel.status == 'need_update')
        for request_model in q.yield_per(1000):
            request = Request(
                url=request_model.url,
                callback=self.parse_update,
                method=request_model.method.upper(),
                headers=pickle.loads(request_model.headers),
                body=pickle.loads(request_model.body),
                cookies=pickle.loads(request_model.cookies),
                meta=pickle.loads(request_model.meta),
                encoding=request_model.encoding,
                dont_filter=True,
                errback=None
            )
            yield request

    def parse_update(self, response):
        """
        """
        item_class = import_item(self.website_rule['class'])
        item = self.get_item(item_class, self.website_rule, response)
        session = self.Session()
        data = self.get_model_data(CarSource, response.url, session)
        if not data:
            self.log(u'找不到CarSource数据{0}'.format(response.url))
            yield None
        else:
            dirty = False
            for field, value in item.items():
                if hasattr(data, field):
                    if not(getattr(data, field) == value):
                        setattr(data, field, value)
                        dirty = True
            if dirty:
                self.update_model_data(data, session)
        yield None

    def get_model_data(self, model_class, url, session):
        """
        """
        return session.query(model_class).filter(model_class.url == url).first()

    def update_model_data(self, data, session):
        session.add(data)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            self.log(u'更新数据时异常：{0}:{1}'.format(unicode(e), data.url), log.ERROR)
        else:
            self.log(u'更新数据完成：{0}'.format(data.url), log.INFO)
