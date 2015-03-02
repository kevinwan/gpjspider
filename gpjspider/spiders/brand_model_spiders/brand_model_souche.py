# -*- coding: utf-8 -*-
import scrapy


class BrandModelSoucheSpider(scrapy.Spider):
    name = "brand_model_souche"
    allowed_domains = ["souche.com"]
    start_urls = (
        'http://www.souche.com/',
    )

    def parse(self, response):
        pass
