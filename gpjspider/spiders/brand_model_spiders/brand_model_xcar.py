# -*- coding: utf-8 -*-
import scrapy


class BrandModelXcarSpider(scrapy.Spider):
    name = "brand_model_xcar"
    allowed_domains = ["used.xcar.com.cn"]
    start_urls = (
        'http://www.used.xcar.com.cn/',
    )

    def parse(self, response):
        pass
