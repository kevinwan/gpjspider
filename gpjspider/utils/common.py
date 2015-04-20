#-*- coding:utf-8 -*-
from scrapy.item import Field
from gpjspider.items import GpjspiderItem
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider


def values(item):
    """
    将 item 的值变成基本元素
    """
    pass


def create_item_class(class_name, field_list):
    """
    动态创建 Item，继承自GpjspiderItem
    """
    fields = {field_name: Field() for field_name in field_list}

    return type(class_name, (GpjspiderItem,), {'fields': fields})


def create_spider_class(class_name, spider_name):
    """
    动态创建 爬虫类，继承自GpjspiderItem
    """
    return type(class_name, (GPJBaseSpider,), {'name': spider_name})
