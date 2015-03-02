# -*- coding: utf-8 -*-
"""
"""
from gpjspider.items import BrandModelItem
from gpjspider.models import BrandModel


class GpjspiderPipeline(object):
    """
    """
    def process_item(self, item, spider):
        for k, v in item.items():
            print u"{0}  ->  {1}".format(k, v)
        return item


class SaveToMySQLPipeline(object):
    """
    把 item 保存到 MySQL。这个 pipeline 应该是最后一个。
    """
    def process_item(self, item, spider):
        if isinstance(item, BrandModelItem):
            o = BrandModel()
            
            o.parent = item['parent']
            o.name = item['name']
            o.url = item['url']
            o.domain = item['domain']
            o.slug = item['slug']
            o.save()
