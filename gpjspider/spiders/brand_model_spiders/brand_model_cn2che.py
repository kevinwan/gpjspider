# -*- coding: utf-8 -*-
import scrapy


class BrandModelCn2cheSpider(scrapy.Spider):
    name = "brand_model_cn2che"
    allowed_domains = ["cn2che.com"]
    start_urls = (
        'http://www.cn2che.com/',
    )

    def parse(self, response):
        pass
