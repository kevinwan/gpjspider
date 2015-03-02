# -*- coding: utf-8 -*-
import scrapy


class BrandModelChe168Spider(scrapy.Spider):
    name = "brand_model_che168"
    allowed_domains = ["che168.com"]
    start_urls = (
        'http://www.che168.com/',
    )

    def parse(self, response):
        pass
