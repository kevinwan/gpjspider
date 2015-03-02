# -*- coding: utf-8 -*-
import scrapy


class BrandModelBaixingSpider(scrapy.Spider):
    name = "brand_model_baixing"
    allowed_domains = ["baixing.com"]
    start_urls = (
        'http://www.baixing.com/',
    )

    def parse(self, response):
        pass
