# -*- coding: utf-8 -*-
"""
"""

import scrapy
from scrapy import Item, Field


class GpjspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BrandModelItem(Item):
    """
    品牌、型号
    """
    parent = Field()
    name = Field()
    domain = Field()
    url = Field()
    slug = Field()


class FourSShopItem(Item):
    """
    """
    shop_name = Field()
    city = Field()
    phone = Field()
    address = Field()
    # 多个品牌用 ###分隔
    brands = Field()
    domain = Field()
    longitude = Field()
    latitude = Field()
    url = Field()
