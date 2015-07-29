# -*- coding: utf-8 -*-
"""
"""
from scrapy import Item, Field


class GpjspiderItem(Item):
    """
    """
    id = Field()
    url = Field()
    domain = Field()


class BrandModelItem(GpjspiderItem):
    """
    品牌、型号
    """
    parent = Field()
    name = Field()
    slug = Field()
    mum = Field()


class FourSShopItem(GpjspiderItem):
    """
    4S 店模型
    """
    shop_name = Field()
    city = Field()
    phone = Field()
    address = Field()
    # 多个品牌用 ###分隔
    brands = Field()
    longitude = Field()
    latitude = Field()


class UsedCarItem(GpjspiderItem):
    """
    优质二手车
    """
    title = Field()
    meta = Field()
    year = Field()
    month = Field()
    time = Field()
    mile = Field()
    volume = Field()
    color = Field()
    control = Field()
    price = Field()
    price_bn = Field()
    brand_slug = Field()
    model_slug = Field()
    model_url = Field()
    city = Field()
    city_slug = Field()
    region = Field()
    region_slug = Field()
    description = Field()
    thumbnail = Field()
    imgurls = Field()
    contact = Field()
    phone = Field()
    company_name = Field()
    company_url = Field()
    status = Field()
    mandatory_insurance = Field()
    business_insurance = Field()
    examine_insurance = Field()
    is_certifield_car = Field()
    transfer_owner = Field()
    condition_level = Field()
    condition_detail = Field()
    car_application = Field()
    driving_license = Field()
    invoice = Field()
    maintenance_record = Field()
    dmodel = Field()
    maintenance_desc = Field()
    quality_service = Field()
    source_type = Field()
    detail_model = Field()
    created_on = Field()


class CarSourceItem(GpjspiderItem):
    price = Field()
    status = Field()




class BaiduHotItem(GpjspiderItem):
    """
    百度指数模型
    """
    keyword = Field()
    is_brand = Field()
    score = Field()
    the_date = Field()