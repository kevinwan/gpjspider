# -*- coding: utf-8 -*-
from django.db import models


class BrandModel(models.Model):
    """
    各个网站的品牌与型号
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    url = models.URLField(max_length=500, default='', blank=True, null=True)
    parent = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='Y')

    source = models.PositiveIntegerField(db_column="source_id", default=1)

    class Meta:
        db_table = 'open_cat_dic'

    def __unicode__(self):
        return self.slug


class FourSShop(models.Model):
    """
    4S 店
    """
    shop_name = models.CharField('名称', max_length=50, blank=True, null=False)
    city = models.CharField(u'城市', max_length=32, blank=True, null=False)
    phone = models.CharField(u'电话', max_length=32, blank=True, null=True)
    address = models.CharField(u'详细地址', max_length=256, blank=True, null=True)
    # 多个品牌用 ###分隔
    brands = models.CharField(u'经营品牌', max_length=128, blank=True, null=True)
    longitude = models.DecimalField(u'经度', decimal_places=6, max_digits=10)
    latitude = models.DecimalField(u'纬度', decimal_places=6, max_digits=10)
    domain = models.CharField(u'来源网站', max_length=32, blank=True, null=True)
    url = models.URLField(max_length=500, default='', blank=True, null=True)

    class Meta:
        db_table = 'open_4s_shop'

    def __unicode__(self):
        return u'<4s {0} {1}>'.format(self.shop_name, self.city)
