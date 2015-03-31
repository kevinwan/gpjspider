# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max

from utils.choices import CONTROL_MODE_CHOICES, SOURCE_TYPE_CHOICES
from utils import constants


class BrandModel(models.Model):
    """
    车辆品牌、型号模型

    唯一性：
    - 品牌：name domain
    - 型号：name parent mum

    1)如果是品牌,那么只看名称,不考虑slug和url
    2)如果是型号,那么要看所属的品牌名称,型号自身名称,生产厂商这三个字段是否一样,都一样就是重复
      ,这条记录就不插入,不考虑slug和url.
    """
    STATUS_CHOICE = (
        ('A', u'待匹配的品牌或型号'),
        ('M', u'已匹配上的品牌或型号'),
        ('N', u'未匹配上的品牌或型号'),
    )
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True)
    domain = models.CharField(max_length=32, blank=True, null=True)
    url = models.URLField(max_length=500, default='', blank=True, null=True)
    parent = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='A')
    mum = models.CharField(u'生产车商', max_length=32, blank=True, null=True)
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


class UsedCar(models.Model):
    """
    UsedCar模型默认过滤掉status为N和T的记录，默认排序为status字段逆序，
            详情见ProductManager,注意查询时无需再过滤status，
            如果需要对多个字段排序，在查询中指定order_by可以覆盖默认排序规则。
    """
    PRODUCT_STATUS_CHOICE = (
        ('M', u'(M)新加入的产品或在后台被修改过'),
        ('N', u'(N)不在前台呈现'),
        ('Q', u'(Q)已售出'),
        ('T', u'(T)重复记录'),
        ('W', u'(W)没有缩略图'),
        ('X', u'(X)没有联系方式'),
        ('Y', u'(Y)信息完整，优先呈现'),
        ('E', u'(E)清理失败'),
    )

    title = models.CharField(u'标题', max_length=200, blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    year = models.IntegerField(u'购置年份', blank=True, default=0)
    month = models.IntegerField(u'购置月份', blank=True, default=6)
    url = models.URLField()
    time = models.DateTimeField(u'发布时间', blank=True, null=True)
    # 爬虫中均已万为单位
    mile = models.DecimalField(
        u'行驶里程', max_digits=5, decimal_places=2, blank=True, null=True
    )
    volume = models.DecimalField(
        u'排量', max_digits=5, decimal_places=1, blank=True, null=True
    )
    color = models.CharField(u'颜色', max_length=32, blank=True, null=True)
    control = models.CharField(
        u'变速箱', choices=CONTROL_MODE_CHOICES, max_length=32, blank=True,
        null=True
    )
    price = models.DecimalField(
        u'预售价格', max_digits=10, decimal_places=1, blank=True, null=True
    )
    # prince_bn : the brand_new price when it was bought
    price_bn = models.DecimalField(
        u'新车购买价格', max_digits=10, decimal_places=1, blank=True, null=True
    )
    brand_slug = models.CharField(
        u'品牌', max_length=32, blank=True, null=True, db_index=True
    )
    model_slug = models.CharField(
        u'型号', max_length=32, blank=True, null=True, db_index=True
    )
    city = models.CharField(u'城市', max_length=50, blank=True, null=True)
    city_slug = models.CharField(
        u'城市slug', max_length=32, blank=True, null=True, db_index=True
    )
    region = models.CharField(u'地址', max_length=50, blank=True, null=True)
    region_slug = models.CharField(
        max_length=32, blank=True, null=True, db_index=True
    )
    description = models.TextField(u'描述', blank=True, null=True)
    # 目前使用thumbnial保存图片的缩略图名称。
    # 缩略图下载之后保存到服务器文件夹IMAGES_STORE = '/home/static/img'
    thumbnail = models.CharField(max_length=200, null=True, blank=True)
    # imgurls用来保存多对应于一部车在源网站多个图片的URL地址，用空格号分开
    imgurls = models.CharField(max_length=4000, null=True, blank=True)
    # image_urls 暂时用于调试(crapy.contrib.pipeline.images.ImagesPipeline)，
    # 没有用在生产环境中
    image_urls = models.CharField(max_length=1024, null=True, blank=True)
    # images 暂时用于调试(crapy.contrib.pipeline.images.ImagesPipeline)，
    # 没有用在生产环境中
    images = models.CharField(max_length=1024, null=True, blank=True)
    # contact info
    contact = models.CharField(u'联系人', max_length=64, blank=True, null=True)
    # phone might be a image url,  a string or a number
    phone = models.CharField(
        u'联系电话', max_length=128, blank=True, null=True, db_index=True
    )
    company_name = models.CharField(
        max_length=128, blank=True, null=True, db_index=True
    )
    company_url = models.URLField(blank=True, null=True, db_index=True)
    # status:'Y'->initial status once crawled,
    # 'N'->unknown,'A'->Active,'I'->Inactive
    status = models.CharField(
        u'状态', max_length=1, blank=True, null=True, default='Y',
        choices=PRODUCT_STATUS_CHOICE
    )
    mandatory_insurance = models.DateTimeField(
        u'交强险到期时间', blank=True, null=True
    )
    business_insurance = models.DateTimeField(
        u'商业险到期时间', blank=True, null=True
    )
    examine_insurance = models.DateTimeField(
        u'年审到期时间', blank=True, null=True
    )
    is_certifield_car = models.BooleanField(u'是否为认证二手车', default=False)
    # u'0表示买的新车，1以上表示买的二手车'
    transfer_owner = models.IntegerField(u'过户次数', blank=True, null=True)
    condition_level = models.CharField(
        u'车况等级', max_length=10, blank=True, null=True
    )
    condition_detail = models.TextField(u'车况介绍', blank=True, null=True)
    # 营运/非营运
    car_application = models.CharField(
        u'车辆用途', max_length=10, blank=True, null=True
    )
    # 是/否
    driving_license = models.CharField(
        u'是否有行驶证', max_length=10, blank=True, null=True
    )
    # 是/否
    invoice = models.CharField(
        u'是否有购车/过户发票', max_length=10, blank=True, null=True
    )
    # 是/否
    maintenance_record = models.CharField(
        u'是否有维修保养记录', max_length=10, blank=True, null=True
    )
    dmodel = models.CharField(
        u'原网站款型', max_length=100, blank=True, null=True, db_index=True
    )
    created_on = models.DateTimeField(
        u'创建时间', auto_now_add=True, blank=True, null=True
    )
    domain = models.CharField(max_length=32, blank=True, null=True)
    detail_model = models.PositiveIntegerField(
        db_column="detail_model_id", default=None
    )
    # 仅仅为了兼容
    checker_runtime = models.PositiveIntegerField(
        db_column="checker_runtime_id", default=1
    )
    maintenance_desc = models.CharField(
        u'保养信息', max_length=256, blank=True, null=True
    )
    # 对于从老爬虫来的车源，默认值是constants.SOURCE_TYPE_OLD_SPIDER
    source_type = models.PositiveIntegerField(
        u'车源类型', choices=SOURCE_TYPE_CHOICES,
        default=constants.SOURCE_TYPE_OLD_SPIDER
    )
    quality_service = models.CharField(
        u'质保服务', max_length=256, blank=True, null=True
    )
    # 没用的字段，just 兼容
    source = models.PositiveIntegerField(db_column="source_id", default=1)

    class Meta:
        db_table = 'open_product_source'

    def __unicode__(self):
        return u'<UsedCar {0} {1}>'.format(self.id, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ("subject", (), {"pid": self.id})

    @classmethod
    def get_max_id(cls):
        prod = cls.objects.aggregate(Max('id'))
        return prod['id__max']

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    def is_private_car(self):
        """
        返回一辆二手车是不是个人车。
        判断标准：
            * company_name 为空
            * company_url 为空
        """
        return not self.company_name and not self.company_url


# class DetailModel(models.Model):
#     """
#     款型
#     """
#     STATUS_CHOICE = (
#         ('A', u'ADD 刚添加的款型'),
#         ('Y', u'YES 确定可投入使用的款型'),
#         ('D', u'DELETE 标记为需要删除的款型'),
#     )
#     HAS_PARAMS = (
#         ('Y', u'YES 有配置参数信息'),
#         ('N', u'NO 无配置参数信息'),
#     )
#     source = models.PositiveIntegerField('source_id', default=0)
#     # 仅仅为了兼容
#     checker_runtime = models.PositiveIntegerField(
#         db_column="checker_runtime_id", default=1
#     )
#     detail_model = models.CharField(
#         max_length=50, blank=True, null=True, db_index=True
#     )
#     detail_model = models.PositiveIntegerField('detail_model_id', default=None)
#     detail_model_slug = models.CharField(
#         max_length=50, blank=True, null=True, unique=True
#     )
#     price_bn = models.DecimalField(
#         max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     url = models.URLField(default='', blank=True, null=True, db_index=True)
#     year = models.IntegerField(blank=True, default=0, verbose_name=u'年款')
#     volume = models.DecimalField(
#         u'排量', max_digits=5, decimal_places=1, blank=True, null=True
#     )
#     global_slug = models.PositiveIntegerField("global_slug_id", default=1)
#     domain = models.CharField(max_length=32, blank=True, null=True)
#     status = models.CharField(
#         max_length=1, blank=True, null=True, default='A', choices=STATUS_CHOICE
#     )
#     has_param = models.CharField(
#         max_length=1, blank=True, null=True, default='N', choices=HAS_PARAMS
#     )
#     listed_year = models.IntegerField(u'上市年份', blank=True, default=0)
#     delisted_year = models.IntegerField(u'退市年份', blank=True, default=0)
#     control = models.CharField(
#         u'变速箱', max_length=32, blank=True, null=True, db_index=True
#     )
#     emission_standard = models.CharField(
#         u'排放标准', max_length=20, blank=True, null=True, db_index=True
#     )

#     def __unicode__(self):
#         return self.detail_model_slug

#     class Meta:
#         db_table = 'open_model_detail'
