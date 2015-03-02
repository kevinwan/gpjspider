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
