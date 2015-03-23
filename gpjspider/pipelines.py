# -*- coding: utf-8 -*-
"""
"""
from gpjspider.items import BrandModelItem, FourSShopItem
from gpjspider.models import BrandModel, FourSShop


class GpjspiderPipeline(object):
    """
    """
    def process_item(self, item, spider):
        for k, v in item.items():
            if v:
                print "{0}  ->  {1}".format(k, v.encode('utf-8'))
            else:
                print "{0}  ->  {1}".format(k, v)
        return item


class SaveToMySQLPipeline(object):
    """
    把 item 保存到 MySQL。这个 pipeline 应该是最后一个。
    """
    def process_item(self, item, spider):
        if isinstance(item, BrandModelItem):
            if not item['parent']:
                o = BrandModel.objects.filter(name=item['name'])
            else:
                o = BrandModel.objects.filter(parent=item['parent'])
                o = o.filter(name=item['name'])
                o = o.filter(mum=item['mum'])
            o = o.filter(domain=item['domain'])
            if not o.all():
                o = BrandModel()
                o.parent = item['parent']
                o.name = item['name']
                o.url = item['url']
                o.domain = item['domain']
                o.slug = item['slug']
                o.mum = item.get('mum')
                o.save()
                spider.log(u'新增 {0} '.format(item['url']))
            else:
                a_o = o.all()[0]
                a_o.parent = item['parent']
                a_o.name = item['name']
                a_o.url = item['url']
                a_o.domain = item['domain']
                a_o.slug = item['slug']
                a_o.mum = item.get('mum')
                a_o.save()
                spider.log(u'{0}对应车型已经存在'.format(item['url']))

        if isinstance(item, FourSShopItem):
            f = FourSShop.objects.filter(shop_name=item['shop_name'])
            f = f.filter(city=item['city'])
            if not f.all():
                o = FourSShop()
                o.shop_name = item['shop_name']
                o.city = item['city']
                o.phone = item['phone']
                o.address = item['address']
                o.brands = item['brands']
                o.domain = item['domain']
                o.longitude = item['longitude']
                o.latitude = item['latitude']
                o.url = item['url']
                o.save()
                spider.log(u'保存 {0}成功'.format(unicode(o)))
            else:
                msg = u'4S店 {0} {1}已经存在'.format(item['shop_name'], item['city'])
                spider.log(msg)
