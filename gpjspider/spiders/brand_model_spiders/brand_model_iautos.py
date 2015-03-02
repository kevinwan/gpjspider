# -*- coding: utf-8 -*-
import scrapy


class BrandModelIautosSpider(scrapy.Spider):
    name = "brand_model_iautos"
    allowed_domains = ["iautos.cn"]
    start_urls = (
        'http://www.iautos.cn/',
    )

    def parse(self, response):
        pass
