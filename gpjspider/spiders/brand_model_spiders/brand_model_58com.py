# -*- coding: utf-8 -*-
import scrapy


class BrandModel58comSpider(scrapy.Spider):
    name = "brand_model_58com"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://www.58.com/',
    )

    def parse(self, response):
        pass
