# -*- coding: utf-8 -*-
"""
去重中间件

"""

import re
from scrapy.exceptions import IgnoreRequest
from scrapy import log
import redis
from gpjspider.utils.url import get_domain
from gpjspider.models import UsedCar
from gpjspider.spiders.high_quality_cars.haoche51 import HighQualityCarHaoche51Spider


redis_conn = redis.StrictRedis()


class FilterReduplicatedMiddleware(object):
    """
    不需要请求的 URL 过滤

    所有过滤函数命名 filter_{domain}
    domain的.替换成_
    """
    def __init__(self, settings):
        if not settings.getlist('FILTER_REDUPLICATED_DOMAINS'):
            self.filter_reduplicated_domians = tuple()
        self.filter_reduplicated_domians = settings.getlist(
            'FILTER_REDUPLICATED_DOMAINS', tuple()
        )
        self.haoche51_filter_key = 'haoche51_filter'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        """
        """
        domain = get_domain(request.url)
        callback_name = ''
        if domain in self.filter_reduplicated_domians:
            callback_name = domain.replace('.', '_')
            cb = getattr(self, 'filter_{0}'.format(callback_name), 'default')
            return cb(request, spider)
        spider.log(u'没有过滤 url {0}'.format(request.url), log.DEBUG)

    def filter_default(self, request, spider):
        """
        默认的过滤函数
        """
        domain = get_domain(request.url)
        msg = 'FilterReduplicatedMiddleware.filter_default:请实现 filter_{0}()'
        msg = msg.format(domain.replace('.', '_'))
        raise IgnoreRequest(msg)

    def filter_haoche51_com(self, request, spider):
        """
        """
        # 列表页直接过滤掉
        if 'vehicle_list' in request.url:
            return None

        try:
            if spider.current_id < 0:
                haoche51_max_id = redis_conn.get(self.haoche51_filter_key)
                haoche51_max_id = int(haoche51_max_id)
                spider.current_id = haoche51_max_id
        except:
            car = UsedCar.objects.filter(domain="haoche51.com")
            car = car.order_by('-id').first()
            if not car:
                raise ValueError(u"haoche51_com's haoche51_max_id is missing.")
            haoche51_max_id = car.id
            redis_conn.set(self.haoche51_filter_key, haoche51_max_id)
            spider.current_id = haoche51_max_id
        gg = re.compile(r"/(\d+)\.html")
        _id = gg.findall(request.url)[0]
        if int(_id) <= spider.current_id:
            raise IgnoreRequest('重复的 URL:{0}'.format(request.url))
        else:
            spider.log('url {0}通过重复性过滤'.format(request.url), log.INFO)
            return None

    def spider_closed(self, spider, reason):
        """
        """
        if isinstance(spider, HighQualityCarHaoche51Spider):
            redis_conn.set(self.haoche51_filter_key, spider.current_id)
