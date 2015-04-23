#-*- coding:utf-8 -*-
from scrapy.item import Field
from gpjspider.items import GpjspiderItem
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.spiders.base_spiders.gpjupdatespider import GPJUpdateSpider
from gpjspider.spiders.base_spiders.incrspider import IncrSpider


def create_item_class(class_name, field_list):
    """
    动态创建 Item，继承自GpjspiderItem
    """
    fields = {field_name: Field() for field_name in field_list}
    return type(class_name, (GpjspiderItem,), {'fields': fields})



def create_spider_class(class_name, spider_name):
    return type(class_name, (GPJBaseSpider,), {'name': spider_name})


def create_full_spider_class(class_name, spider_name):
    return type(class_name, (GPJBaseSpider,), {'name': spider_name})


def create_incr_spider_class(class_name, spider_name):
    return type(class_name, (IncrSpider,), {'name': spider_name})


def create_update_spider_class(class_name, spider_name):
    return type(class_name, (GPJUpdateSpider,), {'name': spider_name})
