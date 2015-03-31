# -*- coding: utf-8 -*-
"""
"""
import re
from datetime import date, datetime
from scrapy import log
from scrapy.exceptions import DropItem
from gpjspider.items import BrandModelItem, FourSShopItem, UsedCarItem
from gpjspider.models import BrandModel, FourSShop
from gpjspider.utils.url import get_domain


class BasePipeline(object):
    """
    """
    def process_item(self, item, spider):
        # for k, v in item.items():
        #     if isinstance(v, list):
        #         item[k] = v[0]
        # for k, v in item.items():
        #     if v:
        #         print "{0}  ->  {1}".format(k, unicode(v).encode('utf-8'))
        #     else:
        #         print "{0}  ->  {1}".format(k, v)
        return item


class GpjspiderPipeline(object):
    """
    """
    def process_item(self, item, spider):
        # spider.log('item:{0}'.format(item))
        if item:
            for k, v in item.items():
                if v:
                    print "{0}  ->  {1}".format(k, unicode(v).encode('utf-8'))
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
        elif isinstance(item, UsedCarItem):
            item.save()
            gg = re.compile(r"/(\d+)\.html")
            _id = gg.findall(item['url'])[0]
            spider.current_id = int(_id)
            spider.log(u'优质二手车 {0}保存成功'.format(item['url']))


class ProcessUsedCarPipeline(object):
    """
    处理优质二手车的第一个 Pipeline。
    """
    def process_item(self, item, spider):
        spider.log(u"ProcessUsedCarPipeline:{0}".format(item), log.INFO)
        if isinstance(item, UsedCarItem):
            # domain = get_domain(item['url'])
            # if 'haoche51.com' in domain:
            #     item = self.process_haoche51(item, spider)
            # elif 'ganji.com' in domain:
            #     item = self.process_ganji(item, spider)
            # elif 'renrenche.com' in domain:
            #     item = self.process_renrenche(item, spider)
            # else:
            item = self.process_default(item, spider)
            return item

    def process_default(self, item, spider):
        """
        """
        return item

    def process_renrenche(self, item, spider):
        item['quality_service'] = item['quality_service'].split('###')
        a = []
        for i in item['quality_service']:
            a.append(i.strip().strip('\r\n').strip())
        item['quality_service'] = '###'.join(a)

        item['month'] = item['month'].split('-')[1]
        item['month'] = int(item['month'])
        item['year'] = item['year'].split('-')[0]
        item['year'] = int(item['year'])
        item['phone'] = item['phone'].strip().strip('\n')
        if u'万公里' in item['mile']:
            item['mile'] = int(item['mile'].strip(u'万公里'))
        item['condition_level'] = item['condition_level'].split(u'：')[0]
        item['condition_level'] = item['condition_level'].strip().strip(u'车况')
        item['brand_slug'] = item['title'].split(u'-')[0].strip()
        item['model_slug'] = item['title'].split(u'-')[1].strip()
        item['model_slug'] = item['model_slug'].split('20')[0].strip()
        if item.get('price_bn'):
            item['price_bn'] = item['price_bn'].strip().split('+')[0]
            item['price_bn'] = item['price_bn'].strip().strip(u'新车万')
            item['price_bn'] = float(item['price_bn'])
        item['region'] = item['region'].strip().split('|')[1].strip()
        item['region'] = item['city'] + item['region']

        imgs = item['imgurls'].split('###')
        a = []
        for img in imgs:
            a.append(img.split('?')[0])
        item['imgurls'] = ' '.join(a)

        item['thumbnail'] = item['thumbnail'].strip().split('?')[0]
        item['price'] = item['price'].strip().strip(u'万').strip(u'￥').strip()
        item['volume'] = item['volume'].split(' ')[0]
        item['transfer_owner'] = item['transfer_owner'].strip().strip(u'次')
        item['transfer_owner'] = int(item['transfer_owner'])
        return item

    def process_ganji(self, item, spider):
        """
        """
        cc = item['brand_slug'].strip().split(u'：')[1]
        item['brand_slug'] = cc.split(u'-')[0].strip()
        item['model_slug'] = cc.split(u'-')[1].strip()
        if u'万公里' in item['mile']:
            item['mile'] = item['mile'].strip(u'万公里')
        item['year'] = item['year'].split('-')[0]
        item['month'] = item['month'].split('-')[1]
        item['region'] = item['city'] + item['region'].strip()
        item['price_bn'] = item['price_bn'].strip().split('+')[0]
        item['price_bn'] = item['price_bn'].split(u'：')[1].strip(u'万')
        return item

    def process_haoche51(self, item, spider):
        """
        """
        spider.log(u"process_haoche51:{0}".format(item), log.INFO)
        year_str = item['year'].replace('\n', '').replace(' ', '')
        year, month = year_str.split('|')[0].replace(u'上牌', '').split('.')
        try:
            year = int(year)
            month = int(month)
        except:
            pass
        else:
            item['year'] = year
            item['month'] = month

        if u'手自一体' in item['control']:
            item['control'] = u'手自一体'
        elif u'手动' in item['control']:
            item['control'] = u'手动'
        elif u'自动' in item['control']:
            item['control'] = u'自动'
        else:
            spider.log(u'control error:{0}'.format(item['control']), log.ERROR)
            item['control'] = ''
        # 行驶3.3万公里
        start_index = item['mile'].find(u"行驶") + len(u'行驶')
        end_index = item['mile'].find(u"万公里")
        mile = item['mile'][start_index:end_index]
        try:
            mile = float(mile)
        except:
            DropItem(u'')
        else:
            item['mile'] = mile

        if u'无' in item['invoice'] or u'没有' in item['invoice']:
            item['invoice'] = u'否'
        else:
            item['invoice'] = u'是'
        if u'无' in item['driving_license'] or u'没有' in item['driving_license']:
            item['driving_license'] = u'否'
        else:
            item['driving_license'] = u'是'
        y = item['mandatory_insurance'].split(u'：')
        year_s = y[1].strip()
        year_start_idx = year_s.find(u'年')
        if year_start_idx != -1:
            year = year_s[:year_start_idx]
            month_start_idx = year_start_idx + len(u'年')
            month_end_idx = year_s.find(u'月')
            month = year_s[month_start_idx: month_end_idx]
            year = int(year.strip())
            month = int(month.strip())
            item['mandatory_insurance'] = date(year, month, 1)
        else:
            spider.log(u'交强险获取不到:{0}'.format(item['mandatory_insurance']), log.ERROR)
            item['mandatory_insurance'] = date.today()

        y = item['examine_insurance'].split(u'：')
        year_s = y[1].strip()
        year_start_idx = year_s.find(u'年')
        if year_start_idx != -1:
            year = year_s[:year_start_idx]
            month_start_idx = year_start_idx + len(u'年')
            month_end_idx = year_s.find(u'月')
            month = year_s[month_start_idx: month_end_idx]
            year = int(year.strip())
            month = int(month.strip())
            item['examine_insurance'] = date(year, month, 1)
        else:
            spider.log(u'年检有效期获取不到:{0}'.format(item['examine_insurance']), log.ERROR)
            item['examine_insurance'] = date.today()

        y = item['business_insurance'].split(u'：')
        year_s = y[1].strip()
        year_start_idx = year_s.find(u'年')
        if year_start_idx != -1:
            year = year_s[:year_start_idx]
            month_start_idx = year_start_idx + len(u'年')
            month_end_idx = year_s.find(u'月')
            month = year_s[month_start_idx: month_end_idx]
            year = int(year.strip())
            month = int(month.strip())
            item['business_insurance'] = date(year, month, 1)
        else:
            spider.log(u'商业险有效期获取不到:{0}'.format(item['business_insurance']), log.ERROR)
            item['business_insurance'] = date.today()

        gg = re.compile(ur'.*过户(\d+)次.*')
        a = gg.findall(item['transfer_owner'])
        if a:
            item['transfer_owner'] = int(a[0])
        else:
            item['transfer_owner'] = 0
        cc = set()
        cl = []
        for i in item['imgurls'].split('###'):
            cc.add(i.split('?')[0])
            if len(cc) > len(cl):
                cl.append(i.split('?')[0])
        item['imgurls'] = ' '.join(cl)
        item['thumbnail'] = cl[0]
        item['brand_slug'] = item['title'].split(u' ')[0]
        item['model_slug'] = item['title'].split(u' ')[1]
        item['condition_level'] = item['condition_level'].strip(u'车况')
        a = item['description'].split('|')
        item['region'] = a[1].strip() + a[2].strip() + item['region'].strip()
        item['contact'] = u'好车无忧'
        if not item.get('time'):
            item['time'] = datetime.now()
        return item
