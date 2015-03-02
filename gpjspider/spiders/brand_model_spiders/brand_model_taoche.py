# -*- coding: utf-8 -*-
import scrapy


class BrandModelTaocheSpider(scrapy.Spider):
    name = "brand_model_taoche"
    allowed_domains = ["taoche.com"]
    start_urls = (
        'http://www.taoche.com/',
    )

    def parse(self, response):
        pass
