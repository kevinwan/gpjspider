#-*- coding: utf-8 -*-
from gpjspider.utils import get_redis_cluster


class CachedCarsPipeline(object):
    def __init__(self, settings):
        if settings.getbool('ENABLE_CACHED_CARS') is None:
            self.enable_cached_cars = True
        self.enable_cached_cars = settings.getbool('ENABLE_CACHED_CARS')
        self.__redis_cluster = get_redis_cluster()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if self.enable_cached_cars:
            self.cache_car(item)
        return item

    def is_duplicated_car(self, usedcar):
        car_str = self.car_str(usedcar)
        keys = self.keys('product_car_*')
        for key in keys:
            if self.sismember(key, car_str):
                return True
        return False

    @classmethod
    def car_str(self, item):
        """
        value:brand_slug#-#model_slug#-#year#-#city#-#mile#-#price
        """
        if (not item['brand_slug'] or not item['model_slug']
            or not item['year'] or not item['city']
            or not item['mile'] or not item['price']):
            return ''
        s = [
            item['brand_slug'], item['model_slug'], str(item['year']),
            item['city'], str(item['mile']), str(item['price'])
        ]
        return u'#-#'.join(s)

    def cache_car(self, item):
        s = self.car_str(item)
        week_num = item['created_on'].isocalendar()[1]
        key = 'product_car_{0}'.format(week_num)
        return self.__redis_cluster.sadd(key, s)
