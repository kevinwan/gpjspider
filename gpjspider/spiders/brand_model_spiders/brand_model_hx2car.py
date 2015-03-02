# -*- coding: utf-8 -*-
import scrapy


class BrandModelHx2carSpider(scrapy.Spider):
    name = "brand_model_hx2car"
    allowed_domains = ["hx2car.com"]
    start_urls = (
        'http://www.hx2car.com/',
    )

    def parse(self, response):
        pass
