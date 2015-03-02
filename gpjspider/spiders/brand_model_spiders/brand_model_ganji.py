# -*- coding: utf-8 -*-
import scrapy


class BrandModelGanjiSpider(scrapy.Spider):
    name = "brand_model_ganji"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://www.58.com/',
    )

    def parse(self, response):
        pass
