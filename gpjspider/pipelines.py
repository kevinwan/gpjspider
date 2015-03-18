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
            print u"{0}  ->  {1}".format(k, v)
        return item


class SaveToMySQLPipeline(object):
    """
    把 item 保存到 MySQL。这个 pipeline 应该是最后一个。
    """
    def process_item(self, item, spider):
        if isinstance(item, BrandModelItem):
            o = BrandModel.objects.filter(parent=item['parent'])
            o = o.filter(name=item['name']).filter(domain=item['domain'])
            o = o.filter(slug=item['slug'])
            o = o.filter(url=item['url'])
            if not o.all():
                o = BrandModel()
                o.parent = item['parent']
                o.name = item['name']
                o.url = item['url']
                o.domain = item['domain']
                o.slug = item['slug']
                o.save()
            else:
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
