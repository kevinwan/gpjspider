# -*- coding: utf-8 -*-
"""
二手车模型
"""
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, CHAR
from sqlalchemy import Boolean, DateTime, Enum, DECIMAL
from gpjspider.utils.constants import SOURCE_TYPE_OLD_SPIDER

from . import Base


class UsedCar(Base):

    """
    UsedCar模型默认过滤掉status为N和T的记录，默认排序为status字段逆序，
            详情见ProductManager,注意查询时无需再过滤status，
            如果需要对多个字段排序，在查询中指定order_by可以覆盖默认排序规则。

        ('odealer', u'一般商家车源'),
        ('dealer', u'商家优质车源'),
        ('cpo', u'厂商认证车源'),
        ('personal', u'一般个人车源'),

    """
    def get_next_update():
        next_update = datetime.now() + timedelta(days=1)
        return next_update

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
    STATUS_CHOICE = (
        #'Y',  # initial status once crawled
        #'N',  # unknown
        #'A',  # Active
        #'I',  # Inactive
        'M',
        'N',
        'Q',
        'T',
        'W',
        'X',
        'Y',
        'E',
        'I',
    )

    __tablename__ = u'open_product_source'
    # __tablename__ = u'open_product_source_tmp'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=True, doc=u'标题')
    meta = Column(Text, nullable=True)
    year = Column(Integer, nullable=True, default=0, doc=u'购置年份')
    month = Column(Integer, nullable=True, default=6, doc=u'购置月份')
    url = Column(String(500), default='', index=True, nullable=True)
    time = Column(DateTime, nullable=True, doc=u'发布时间')
    # 爬虫中均已万为单位
    mile = Column(DECIMAL(precision=5, scale=2), doc=u'行驶里程')
    volume = Column(DECIMAL(precision=5, scale=2), doc=u'排量')
    color = Column(String(32), default='', nullable=True, doc=u'颜色')
    # choices=CONTROL_MODE_CHOICES  变速箱
    control = Column(String(32), default='', nullable=True, doc=u'变速箱')
    price = Column(DECIMAL(precision=10, scale=2), doc=u'预售价格')
    # prince_bn : the brand_new price when it was bought
    price_bn = Column(DECIMAL(precision=10, scale=2), doc=u'新车购买价格')
    brand_slug = Column('brand_slug', String(32), index=True, doc=u'品牌')
    model_slug = Column('model_slug', String(32), index=True, doc=u'型号')
    model_url = Column(String(500), nullable=True)
    city = Column(String(50), doc=u'城市')
    city_slug = Column(String(32), index=True, doc=u'城市slug')
    region = Column(String(50), index=True, doc=u'地址')
    region_slug = Column(String(32), index=True, doc=u'地址slug')
    description = Column(Text, doc=u'描述')
    # 目前使用thumbnial保存图片的缩略图名称。
    # 缩略图下载之后保存到服务器文件夹IMAGES_STORE = '/home/static/img'
    thumbnail = Column(String(200), nullable=True, doc=u'描述')
    # imgurls用来保存多对应于一部车在源网站多个图片的URL地址，用空格号分开
    imgurls = Column(String(4000), nullable=True, doc=u'图片')
    contact = Column(String(64), nullable=True, doc=u'联系人')
    # phone might be a image url,  a string or a number
    phone = Column(String(128), index=True, nullable=True, doc=u'联系电话')
    company_name = Column(String(128), index=True, nullable=True)
    company_url = Column(String(500), index=True, nullable=True)
    # status = Column(
        # Enum(STATUS_CHOICE), index=True, default='Y', nullable=True, doc=u'状态')
    status = Column(String(32), index=True, default='Y', nullable=True, doc=u'状态')
    mandatory_insurance = Column(
        DateTime, default=None, nullable=True, doc=u'交强险到期时间')
    business_insurance = Column(
        DateTime, default=None, nullable=True, doc=u'商业险到期时间')
    examine_insurance = Column(
        DateTime, default=None, nullable=True, doc=u'年审到期时间')
    is_certifield_car = Column(Boolean, default=True, doc=u'是否为认证二手车')
    # u'0表示买的新车，1以上表示买的二手车'
    transfer_owner = Column(Integer, default=0, doc=u'过户次数')
    condition_level = Column(String(10), default='', doc=u'车况等级')
    condition_detail = Column(Text, default='', doc=u'车况介绍')
    # 营运/非营运
    car_application = Column(String(10), default=u'非营运', doc=u'车辆用途')
    # 是/否
    driving_license = Column(String(10), doc=u'是否有行驶证')
    # 是/否
    invoice = Column(String(10), doc=u'是否有购车/过户发票')
    # 是/否
    maintenance_record = Column(String(10), doc=u'是否有维修保养记录')
    dmodel = Column(String(10), index=True, doc=u'原网站款型')
    created_on = Column(DateTime, default=datetime.now, doc=u'创建时间')
    domain = Column(String(32), nullable=True, doc=u'来源网站')
    maintenance_desc = Column(String(256), doc=u'保养信息')
    # 对于从老爬虫来的车源，默认值是constants.SOURCE_TYPE_OLD_SPIDER
    source_type = Column(
        String(256), default=SOURCE_TYPE_OLD_SPIDER, doc=u'车源类型')
    quality_service = Column(String(256), default='', doc=u'质保服务')
    # 没用的字段，just 兼容
    source = Column("source_id", Integer, default=1)
    detail_model = Column("detail_model_id", Integer, default=None)
    checker_runtime = Column("checker_runtime_id", Integer, default=1)
    last_update = Column(DateTime, default=datetime.now, doc=u'上次更新时间时间')
    next_update = Column(DateTime, default=get_next_update, doc=u'下次更新时间时间')
    update_count = Column(Integer, default=0, doc=u'更新次数')


class RawSellDealer(Base):
    """
    商家匹配
    """
    __tablename__ = u'raw_sell_dealer'

    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, doc=u'匹配的id', nullable=True, )
    company_name = Column(String(50), nullable=True, doc=u'名称')
    company_url = Column(String(500), nullable=True, default='')
    city = Column(String(32), nullable=True, doc=u'城市')
    contact = Column(String(32), nullable=True, doc=u'联系人')
    phone = Column(String(32), nullable=True, doc=u'电话')
    address = Column(String(256), nullable=True, doc=u'详细地址')
    domain = Column(String(32), nullable=True, doc=u'来源网站')
    status = Column(Integer, doc=u'状态', default=0)

    def __unicode__(self):
        return u'<RawSellDealer {0} {1} - {2} >'.format(self.company_name, self.city, self.dealer_id)
#
# class CarFingerprint(Base):
#     """
#     车辆指纹数据
#     """
#     __tablename__ = u'car_fingerprint'
#
#     id = Column(Integer, primary_key=True)
#     detail = Column(String(500), nullable=False, default='', doc=u'详细数据')
#     sig = Column(CHAR(32), unique=True, nullable=False, doc=u'摘要指纹')
#     cnt = Column(Integer, doc=u'数量', default=0)
#
#     def __unicode__(self):
#         return u'<CarFingerprint {0} {1} >'.format(self.defailt, self.cnt)
#
