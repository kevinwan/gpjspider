# -*- coding: utf-8 -*-
import os
import traceback
import json
from copy import deepcopy
import tempfile
import scrapy
from scrapy import log
from gpjspider.items import BrandModelItem


class BrandModel2scSohuSpider(scrapy.Spider):
    name = "brand_model_2sc_sohu"
    allowed_domains = ["2sc.sohu.com"]
    start_urls = (
        'http://2sc.sohu.com/interface/common/getbrandmodstr/?nation=0&type=0',
    )

    def parse(self, response):
        c = response.body_as_unicode()
        f = tempfile.NamedTemporaryFile(prefix='gpjspider')
        f.write('a=')
        f.write(c.encode('utf-8'))
        f.write(';var b = JSON.stringify(a);console.log(b);')
        f.flush()
        try:
            os.system('js {0} >/tmp/z.log'.format(f.name))
        except:
            s = traceback.format_exc()
            self.log(u'执行 nodejs 出错:{0}'.format(s), level=log.ERROR)
            yield None
        finally:
            f.close()

        try:
            json_str = open('/tmp/z.log').read()
        except:
            pass
        else:
            js = json.loads(json_str)
            for j in js:
                item = BrandModelItem()
                item['domain'] = '2sc.sohu.com'
                item['slug'] = j['e']
                item['parent'] = j['n'].strip().split(' ')[-1]
                item['url'] = 'http://2sc.sohu.com/auto-{0}/'.format(item['slug'])
                item['name'] = None
                for ii in j['s']:
                    for mm in ii['b']:
                        model_item = deepcopy(item)
                        model_item['name'] = mm['n']
                        model_item['slug'] = mm['e']
                        model_item['url'] = 'http://2sc.sohu.com/auto1-{0}/'.format(mm['e'])
                        yield model_item
                item['name'] = item['parent']
                item['parent'] = None
                yield item
