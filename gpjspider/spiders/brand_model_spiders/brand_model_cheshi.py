# -*- coding: utf-8 -*-
import scrapy


class BrandModelCheshiSpider(scrapy.Spider):
    name = "brand_model_cheshi"
    allowed_domains = ["cheshi.com"]
    start_urls = (
        'http://www.cheshi.com/',
    )

    def parse(self, response):
        pass
