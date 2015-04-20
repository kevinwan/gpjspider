# -*- coding: utf-8 -*-
"""
实现各种请求去重过滤器
"""
from __future__ import print_function
import os

from scrapy import log
from scrapy.utils.job import job_dir
from scrapy.utils.request import request_fingerprint
from scrapy.dupefilter import BaseDupeFilter


class DomainRequestDupeFilter(BaseDupeFilter):
    """基于域名和请求的去重过滤器
    和 scrapy 提供的去重过滤器不一样的地方是：
    1. 按 domain 保存指纹，减小指纹库规模
    2. 根据 domain 加载指纹库，减小内存占用
    """

    def __init__(self, path=None, debug=False):
        self.file = None
        self.fingerprints = set()
        self.logdupes = True
        self.debug = debug
        if path:
            self.file = open(os.path.join(path, 'requests.seen'), 'a+')
            self.fingerprints.update(x.rstrip() for x in self.file)

    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(job_dir(settings), debug)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)

    def request_fingerprint(self, request):
        """
        计算指纹时加入cookies
        """
        return request_fingerprint(request, include_headers=('Cookie'))

    def close(self, reason):
        if self.file:
            self.file.close()

    def log(self, request, spider):
        if self.debug:
            fmt = "Filtered duplicate request: %(request)s"
            log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)
        elif self.logdupes:
            fmt = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            log.msg(format=fmt, request=request, level=log.DEBUG, spider=spider)
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
