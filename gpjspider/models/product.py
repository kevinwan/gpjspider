# -*- coding: utf-8 -*-
"""
产品用的数据表定义

用于将原始数据清理之后保存到产品表


[15/4/14 17:12:47] 彭博: open_model_detail存的公平价的款型信息
[15/4/14 17:13:10] 彭博: model_detail_normal存的公平价款型和第三方款型的映射信息
"""

from datetime import datetime,timedelta
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, DECIMAL, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session

from . import Base

TRADE_CAR_ALIVE_DURATION = {
    'days': 12,
}

class CategoryDict(Base):

    """
    各个网站汽车品牌，型号库
    """
    __tablename__ = u'open_cat_dic'

    STATUS_CHOICE = (
        'A',  # 待匹配的品牌或型号
        'M',  # 已匹配上的品牌或型号
        'N',  # 未匹配上的品牌或型号
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    slug = Column(String(32), nullable=True)
    global_name = Column(String(50), nullable=True)
    domain = Column(String(32), nullable=True)
    url = Column(String(256), nullable=True, default='')
    parent = Column(String(32), nullable=True)
    mum = Column(String(32), nullable=True, doc=u'生产车商')
    classified = Column(String(32), nullable=True)
    classified_url = Column(String(256), nullable=True)
    keywords = Column(Text, nullable=True)
    status = Column(Enum(STATUS_CHOICE), default='A')
    # One To Many
    global_slug = Column(String(32), ForeignKey('open_category.slug'))

    def is_brand(self):
        return not self.parent

    def is_model(self):
        return bool(self.parent)

    def get_brandname(self):
        if self.is_brand():
            return None
        return self.parent

    def get_brand(self):
        if self.is_brand():
            return None
        session = object_session(self)
        return session.query(self.__class__).filter(
            self.__class__.name == self.parent).filter(
            self.__class__.parent is None).first()

    def __unicode__(self):
        if self.parent:
            return u'<CategoryDict {0} {1}>'.format(self.parent, self.name)
        else:
            return u'<CategoryDict {0}>'.format(self.name)


class Category(Base):

    """
    公平价汽车品牌、型号库(产品级)
    """
    __tablename__ = u'open_category'

    CLASSIFIED_CHOICE = (
        u'微型车',
        u'小型车',
        u'紧凑型车',
        u'中型车',
        u'中大型车',
        u'豪华型车',
        u'小型SUV',
        u'紧凑型SUV',
        u'中型SUV',
        u'中大型SUV',
        u'全尺寸SUV',
        u'MPV',
        u'跑车',
        u'微面',
        u'微卡',
        u'轻客',
        u'皮卡',
    )
    STATUS_CHOICE = (
        'A',  # ADD 刚添加的品牌或型号
        'Y',  # YES 确定投入使用的品牌或型号
        'D',  # DELETE 标记为需要删除的品牌或型号
    )

    ATTRIBUTE_CHOICE = (
        u'合资',
        u'进口',
        u'国产',
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True, doc=u'型号/品牌（中文名）')
    first_letter = Column(String(1), nullable=True, doc=u'首字母')
    slug_global = Column(String(32), nullable=True)
    slug = Column(String(32), nullable=True, unique=True, doc=u'型号/品牌（英文简写）')
    url = Column(String(256), nullable=True, default='')
    #  forign key
    # parent = models.ForeignKey('Category', to_field='slug', db_column='parent',
    #                            max_length=32, nullable=True, null=True,
    #                            related_name='models',
    #                            doc=u'品牌（英文简写）')
    parent = Column(String(32), nullable=True)
    mum = Column(String(32), nullable=True, doc=u'生产车商')
    classified = Column(Enum(CLASSIFIED_CHOICE), nullable=True, doc=u'级别')
    classified_url = Column(String(256), nullable=True)
    keywords = Column(String(100), nullable=True, index=True)
    logo_img = Column(String(200), nullable=True)
    thumbnail = Column(String(200), nullable=True, index=True, doc=u'缩略图')
    has_detailmodel = Column(Integer, nullable=True, default=0)
    score = Column(Integer, nullable=True, default=0)
    starting_price = Column(
        DECIMAL(precision=10, scale=1), nullable=True, default=0, doc=u'起步价格')
    classified_slug = Column(String(128), nullable=True)
    pinyin = Column(String(32), nullable=True, index=True, doc=u'型号/品牌(拼音)')
    status = Column(Enum(STATUS_CHOICE), nullable=True, default='A')
    attribute = Column(
        Enum(ATTRIBUTE_CHOICE), nullable=True, index=True, default='A',
        doc=u'属性，区分国产还是进口等'
    )
    units = Column(Integer, default=0, doc=u'参与统计的该型号车源数量')

    # One to Many
    normalmodeldetails = relationship("NormalModelDetail", backref="category")
    category_dicts = relationship("CategoryDict", backref="category")
    model_details = relationship("ModelDetail", backref="category")

    def get_detail_model(self, detail_model):
        """
        获取款型
        """
        pass

    def __unicode__(self):
        if self.parent:
            return u'<CategoryDict {0} {1}>'.format(self.parent, self.name)
        else:
            return u'<CategoryDict {0}>'.format(self.name)


class ModelDetail(Base):

    """
    公平价款型
    """
    __tablename__ = u'open_model_detail'

    STATUS_CHOICE = (
        'A',  # ADD 刚添加的款型
        'Y',  # YES 确定可投入使用的款型
        'D',  # DELETE 标记为需要删除的款型
    )
    HAS_PARAMS = (
        'Y',  # YES 有配置参数信息
        'N',  # NO 无配置参数信息
    )

    id = Column(Integer, primary_key=True)
    detail_model = Column(String(50), nullable=True, index=True)
    detail_model_slug = Column(
        String(50), nullable=True, index=True, unique=True)
    price_bn = Column(DECIMAL(precision=10, scale=2), nullable=True)
    url = Column(String(256), nullable=True, default='', index=True)
    year = Column(Integer, nullable=True, default=0, doc=u'年款')
    volume = Column(DECIMAL(precision=5, scale=1), nullable=True, doc=u'排量')
    domain = Column(String(32), nullable=True)
    status = Column(Enum(STATUS_CHOICE), nullable=True, default='A')
    has_param = Column(Enum(HAS_PARAMS), nullable=True, default='N')
    listed_year = Column(Integer, nullable=True, default=0, doc=u'上市年份')
    delisted_year = Column(Integer, nullable=True, default=0, doc=u'退市年份')
    control = Column(String(32), nullable=True, index=True, doc=u'变速箱')
    emission_standard = Column(
        String(20), nullable=True, index=True, doc=u'排放标准')

    global_slug = Column(Integer, ForeignKey('open_category.slug'))
    normal_model_details = relationship(
        "NormalModelDetail", backref="obj_model_detail")


class NormalModelDetail(Base):

    """
    保存第三方网站款型和公平价款型的映射信息
    """
    __tablename__ = u'model_detail_normal'

    STATUS_CHOICES = (
        'P',  # 还没有匹配
        'U',  # 没有对应的匹配项
        'M',  # 已手动匹配并成功匹配
        'F',  # 已手动匹配但未成功匹配
        'A',  # 程序完成的匹配
    )

    id = Column(Integer, primary_key=True)
    brand = Column(String(20), index=True, nullable=True, doc=u'原网站品牌')
    model = Column(String(100), index=True, nullable=True, doc=u'原网站型号')
    manufactor = Column(String(20), index=True, nullable=True, doc=u'原网站厂商')
    global_name = Column(String(20), index=True, nullable=True, doc=u'公平价型号')
    model_detail = Column(String(100), index=True, nullable=True, doc=u'原网站款型')
    year = Column(Integer, default=0, nullable=True, doc=u'原网站款型年款')
    price = Column(
        DECIMAL(precision=10, scale=1), default=0, nullable=True,
        doc=u'原网站款型新车指导价'
    )
    domain = Column(String(20), index=True, nullable=True, doc=u'原网站域名')
    # domain = Column(String(20), index=True, nullable=True, doc=u'原网站域名')
    status = Column(Enum(STATUS_CHOICES), default='P', doc=u'匹配的状态')
    volume = Column(DECIMAL(precision=5, scale=1), index=True, doc=u'排量')
    model_detail_origin_id = Column(Integer, default=0, doc=u'原网站款型id')
    # One To Many
    global_slug = Column(String(32), ForeignKey('open_category.slug'))
    model_detail_slug_id = Column(Integer, ForeignKey('open_model_detail.id'))
    # global_slug = models.ForeignKey('Category', to_field='slug',
    # null=True, db_column='global_slug', doc=u'公平价型号slug')

    # model_detail_slug = models.ForeignKey('Model_detail', null=True, doc=u'公平价款型id')


class CarSource(Base):

    """
    优质二手车基本信息
    """
    CAR_SOURCE_STATUS_CHOICES = (
        'sale',    #
        'review',  #
    )

    CAR_SOURCE_TYPE_CHOICES = (
        'dealer',    # 商家车源
        'cpo',       # 认证车源
        'personal',  # 个人车源
        'odealer',   #
    )

    __tablename__ = u'car_source'

    id = Column(Integer, primary_key=True)
    url = Column(String(256), nullable=True, doc=u'原始链接')
    title = Column(String(200), nullable=True, doc=u'标题')
    pub_time = Column(DateTime, default=datetime.now, doc=u'发布时间')
    # brand_slug, model_slug, model_detail_slug存放对应的 slug，而非汉字
    brand_slug = Column(String(32), index=True, nullable=True, doc=u'品牌')
    model_slug = Column(String(32), index=True, nullable=True, doc=u'型号')
    model_detail_slug = Column(
        String(32), index=True, nullable=True, doc=u'详细款型'
    )
    mile = Column(DECIMAL(precision=5, scale=2), doc=u'行驶里程')
    year = Column(Integer, nullable=True, default=2000, doc=u'上牌年份')
    month = Column(Integer, nullable=True, default=6, doc=u'上牌月份')
    dealer_id = Column(Integer, nullable=True, default=0, doc=u'匹配的商家')
    control = Column(String(32), index=True, nullable=True, doc=u'变速箱')
    city = Column(String(50), index=True, nullable=True, doc=u'城市')
    price = Column(
        DECIMAL(precision=5, scale=2), index=True, nullable=True, doc=u'售价')
    volume = Column(
        DECIMAL(precision=5, scale=1), index=True, nullable=True, doc=u'排量')
    color = Column(String(32), nullable=True, doc=u'颜色')
    thumbnail = Column(String(256), nullable=True, doc=u'缩略图链接')
    #  yanzheng
    phone = Column(String(20), index=True, nullable=True, doc=u'联系电话')
    domain = Column(String(32), nullable=True, doc=u'来源网站域名')
    # 商家优质车/认证车/个人车
    source_type = Column(
        Enum(CAR_SOURCE_TYPE_CHOICES), default='', index=True,
        nullable=True, doc=u'来源'
    )
    status = Column(
        # Enum(CAR_SOURCE_STATUS_CHOICES),
        index=True, default='',
        nullable=True, doc=u'状态'
    )
    province = Column(String(32), nullable=True)
    process_status = Column(String(1), default='P')
    qs_tags = Column(String(32), nullable=True, default=None)
    eval_price = Column(DECIMAL(precision=5, scale=2), default=0,
                        doc=u'估值价格(万元)')
    gpj_index = Column(DECIMAL(precision=5, scale=2), default=0)
    # One to One
    car_detail = relationship("CarDetailInfo", uselist=False, backref="car")
    #car_detail = relationship("CarDetailInfo", uselist=False, backref="car", onupdate="cascade")
    # One to Many
    images = relationship("CarImage", backref="car")

    def __unicode__(self):
        return u'<CarSource {0}>'.format(self.id)

    __str__ = __unicode__

    @classmethod
    def mark_offline(cls, session, old_item_ids=None):
        from gpjspider.utils.misc import  conver_item_ids
        old_item_ids = conver_item_ids(old_item_ids, cls.__name__)
        if old_item_ids:
            # 旧的标记下线
            session.query(cls).filter(cls.id.in_(old_item_ids)).update(dict(status='review'), synchronize_session=False)
            return True
        return False

    @classmethod
    def mark_duplicate(cls, session, item_id, old_item_ids=None):
        if old_item_ids:
            # 旧的标记未已经下线，把新的标记未上线
            if cls.mark_offline(session, old_item_ids):
                session.query(cls).filter_by(id=item_id).update(dict(status='sale'), synchronize_session=False)
        else:
            session.query(cls).filter_by(id=item_id).update(dict(status='review'), synchronize_session=False)



class CarDetailInfo(Base):

    """
    优质二手车详细信息
    """
    __tablename__ = u'car_detail_info'

    id = Column(Integer, primary_key=True)
    update_time = Column(DateTime, default=datetime.now, doc=u'更新时间')
    condition = Column(String(20), nullable=True, doc=u'车况等级')
    condition_score = Column(String(10), nullable=True, doc=u'车况分数')
    description = Column(Text, nullable=True, doc=u'描述')
    contact = Column(String(64), nullable=True, doc=u'联系人')
    region = Column(String(50), nullable=True, doc=u'地址')
    company_name = Column(String(128), nullable=True, doc=u'商家名称')
    mandatory_insurance = Column(DateTime, nullable=True, doc=u'交强险到期时间')
    business_insurance = Column(DateTime, nullable=True, doc=u'商业险到期时间')
    examine_insurance = Column(DateTime, nullable=True, doc=u'年检到期时间')
    transfer_owner = Column(String(10), nullable=True, doc=u'过户次数')
    maintenance = Column(String(100), nullable=True, doc=u'保养情况')
    insurance_money = Column(
        DECIMAL(precision=5, scale=2), index=True, nullable=True, doc=u'最高维修费(万元)')
    car_key = Column(String(10), nullable=True, doc=u'车钥匙数量')
    quality_assurance = Column(String(50), nullable=True, doc=u'提供质保的信息')

    # One to One
    car_id = Column(Integer, ForeignKey('car_source.id'), onupdate="cascade")

    def __repr__(self):
        return "<CarDetailInfo {0}>".format(self.id)

    def __unicode__(self):
        return u'<CarDetailInfo {0}>'.format(self.id)

    __str__ = __unicode__


class CarImage(Base):

    """
    优质二手车图片信息
    """
    __tablename__ = u'car_image'

    IMAGE_NAME_CHOICES = (
        'driving_license',  # 行驶证
    )

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey('car_source.id'), onupdate="cascade")
    image_name = Column(
        Enum(IMAGE_NAME_CHOICES), default='', nullable=True, doc=u'图片名'
    )
    image = Column(String(256), nullable=True, doc=u'图片路径地址')
    create_time = Column(DateTime, default=datetime.now, doc=u'创建时间')

    def __repr__(self):
        return "<CarImage {0}>".format(self.id)

    def __unicode__(self):
        return u'<CarImage {0} {1}>'.format(self.car, self.image_name)

    __str__ = __unicode__


class City(Base):

    """
    公平价 City 库
    """
    __tablename__ = u'open_city'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True, index=True)
    slug = Column(String(32), nullable=True, index=True)
    pinyin = Column(String(32), nullable=True, index=True)
    quhao = Column(String(32), nullable=True, index=True, doc=u'区号')
    url = Column(String(500), default='', nullable=True)
    parent = Column(String(50), nullable=True, index=True)
    priority = Column(Integer, nullable=True)
    longitude = Column(DECIMAL(precision=5, scale=2), nullable=True)
    latitude = Column(DECIMAL(precision=5, scale=2), nullable=True)
    # 没用的字段，just 兼容
    source = Column("source_id", Integer, default=1)
    checker_runtime = Column("checker_runtime_id", Integer, default=1)

    def is_city(self):
        return self.parent != 0

    def is_province(self):
        return self.parent == 0

    def get_province(self):
        if self.is_province():
            return None
        session = object_session(self)
        return session.query(self.__class__).filter(
            self.__class__.id == int(self.parent)).first()

    def __unicode__(self):
        if self.parent:
            return u'<City {0} {1}>'.format(self.parent, self.name)
        else:
            return u'<City {0}>'.format(self.name)


class ByYearVolume(Base):
    __tablename__ = u'open_by_year_volume'

    SOURCE_TYPE_CHOICE = (
        'C',  # (Company)车商车源统计结果
        'P',  # (Person)个人车源统计结果
    )

    id = Column(Integer, primary_key=True)
    avg_price = Column(
        DECIMAL(precision=10, scale=1), nullable=True, doc=u'平均标价')
    units = Column(Integer, default=0, nullable=False, doc=u'参与统计的车源数量')
    year = Column(Integer, default=0, nullable=False, index=True)
    volume = Column(
        DECIMAL(precision=5, scale=1), default=None, index=True, doc=u'排量')
    price_range_min = Column(DECIMAL(precision=10, scale=1), nullable=True)
    price_range_max = Column(DECIMAL(precision=10, scale=1), nullable=True)
    depreciation_rate = Column(DECIMAL(precision=5, scale=4), nullable=True)
    avg_price_bn = Column(
        DECIMAL(precision=10, scale=1), default=None, doc=u'同排量下的平均新车指导价')
    avg_tradein_price = Column(
        DECIMAL(precision=10, scale=1), default=None, doc=u'平均的商家收购价')
    theoretic_tradein_price = Column(
        DECIMAL(precision=10, scale=1), default=None)
    source = Column(Enum(SOURCE_TYPE_CHOICE), nullable=True, doc=u'统计来源')
    brand_slug = Column(String(32), default=None, index=True)
    model_slug = Column(String(32), default=None, index=True)

    def __unicode__(self):
        return u'<ByYearVolume {0} {1} {2}>'.format(
            self.brand_slug, self.model_slug, self.year, self.volume)

    __repr__ = __unicode__


class TradeCar(Base):

    __tablename__ = 'open_sell_car'

    TRADE_CAR_STATUS_CHOICES = (
        ('A', u'原始数据'),
        ('N', u'新添加'),
        ('F', u'无效'),
        ('C', u'已联系上车主'),
        ('W', u'已清洗确认'),
        ('D', u'已对接商家'),
        ('S', u'已出售'),
    )
    TRADE_CAR_SOURCE_CHOICE = (
        ('web_pc', u'来自网站'),
        ('web_responsive', u'来自响应式网站'),
        ('android', u'来自Android客户端'),
        ('ios', u'来自IOS客户端'),
        ('crawler', u'来自推送'),
    )
    INTENT_CHOICES = (
        ('sell', u'卖车'),
        ('buy', u'买车')
    )
    CONDITION_CHOICE = (
        ('fair', u'一般'),
        ('good', u'较好'),
        ('excellent', u'优秀')
    )

    id = Column(Integer, primary_key=True)
    contact = Column(String(20), default='', nullable=True,
                     doc=u'联系人')
    email = Column(String(30), default='', doc=u'邮箱地址')
    phone = Column(String(20), nullable=True, doc=u'联系电话')
    brand = Column(String(32), doc=u'品牌slug')
    model = Column(String(32), doc=u'型号slug')
    model_detail = Column(String(32), doc=u'款型slug')
    year = Column(Integer, default=0, doc=u'上牌年份')
    month = Column(Integer, default=6, doc=u'上牌月份')
    mile = Column(Integer, default=0, doc=u'行驶里程(公里)')
    condition = Column(Enum(CONDITION_CHOICE), default='good', doc=u'车况')
    condition_detail = Column(String(50), default='',
                              doc=u'具体车况分数')
    color = Column(String(20), default='', nullable=True, doc=u'颜色')
    option = Column(String(30), default='0-0-0-0', doc=u'配置')
    city = Column(String(50), nullable=True, doc=u'城市')
    district = Column(String(30), default='', doc=u'区域')
    status = Column(Enum(TRADE_CAR_STATUS_CHOICES),
                    nullable=True, default='A', doc=u'状态')
    source = Column(
        Enum(TRADE_CAR_SOURCE_CHOICE), nullable=True, default='crawler', doc=u'来源')
    created_on = Column(DateTime, default=datetime.now, doc=u'创建时间')
    updated_on = Column(DateTime, default=datetime.now, doc=u'更新时间')
    intent = Column(
        Enum(INTENT_CHOICES), default='sell', nullable=True, doc=u'买卖意图')
    list_price = Column(DECIMAL(precision=5, scale=2),
                        default=0, doc=u'心理价位(万元)')
    eval_price = Column(DECIMAL(precision=5, scale=2), default=0,
                        doc=u'估值价格(万元)')
    note = Column(String(200), default='', nullable=True,
                  doc=u'备注')
    car_id = Column(Integer, default=0, doc=u'车源id')
    source_site = Column(String(20), default='', doc=u'标记')
    send_sms = Column(Boolean, default=False, doc=u'发送短信')
    send_sms_status = Column(Boolean, default=False, doc=u'发送短信状态')
    access_report = Column(Boolean, default=False, doc=u'访问估值报告')
    mandatory_insurance = Column(
        DateTime, default=None, nullable=True, doc=u'交强险到期时间')
    examine_insurance = Column(
        DateTime, default=None, nullable=True, doc=u'年检到期时间')
    inner_color = Column(String(20), default='', doc=u'车内饰颜色')
    car_owner = Column(String(10), default='', doc=u'车是在名下')
    loan = Column(String(10), default='', doc=u'车是否贷款')
    insurance_money = Column(String(20), default='', doc=u'最大一次出险金额')
    modify_car = Column(String(10), default='', doc=u'外观是否改装')
    transfer_owner = Column(String(10), default='', doc=u'是否过户')
    maintenance = Column(String(100), default='', doc=u'保养情况')
    commercial_insurance = Column(
        Boolean, default=False, doc=u'商业险是否随车卖')

    @staticmethod
    def init(item):
        trade_car = TradeCar()
        for attr in 'year month city volume phone mandatory_insurance examine_insurance'.split():
            setattr(trade_car, attr, item[attr])
        trade_car.car_id = item['id']
        trade_car.contact = item['contact'] or ''
        trade_car.brand = item['brand_slug']
        trade_car.model = item['model_slug']
        trade_car.list_price = item['price']
        trade_car.source_site = item['domain']
        try:
            mile = item['mile']
            mile = float(mile)
        except:
            trade_car.mile = mile
        else:
            trade_car.mile = int(10000 * mile)
        # trade_car.created_on = item['time']
        # trade_car.created_on = item['created_on']
        # 150813 @yibo
        trade_car.created_on = datetime.now()

        trade_car.color = item['color'] or ''
        if item['detail_model']:
            detail_model_slug = item['detail_model']
        else:
            detail_model_slug = '-'.join(['all-standard',
                                          str(item['volume']).replace('.', '_')])
        trade_car.model_detail = detail_model_slug
        return trade_car

    @classmethod
    def last_dup_item_is_alive(cls, session, old_item_ids=None):
        from gpjspider.utils.misc import  conver_item_ids
        old_item_ids = conver_item_ids(old_item_ids, cls.__name__)
        if old_item_ids:
            expire_time = datetime.now() - timedelta(**TRADE_CAR_ALIVE_DURATION)
            old_item_ids = map(int, old_item_ids)
            cnt =session.query(cls).filter(cls.car_id.in_(old_item_ids), cls.created_on>expire_time).count()
            if cnt>0:
                return True
        return False

    @classmethod
    def mock_dup_car(cls, session):
        from .usedcars import UsedCar
        import time
        ts = str(time.time())
        expire_time = datetime.now() - timedelta(**TRADE_CAR_ALIVE_DURATION)

        # should go in
        base_query = session.query(cls.car_id)
            # .filter(cls.city.in_([u'北京',u'成都', u'南京']))
        car_id = base_query.filter(cls.created_on<expire_time).order_by(cls.id.desc()).limit(1).scalar()

        data = {k:v for k,v in session.query(UsedCar).filter_by(id=car_id).first().__dict__.items() if not k.startswith('_')}
        del data['id']


        data['url']='%s#should_go_in%s' % (data['url'],ts)
        data['created_on']=datetime.now()
        data['source_type']=4
        data['city']=u'成都'


        expired_item=UsedCar(**data)
        session.add(expired_item)

        # should not go in
        car_id = base_query.filter(cls.created_on>expire_time).order_by(cls.id.asc()).limit(1).scalar()

        data = {k:v for k,v in session.query(UsedCar).filter_by(id=car_id).first().__dict__.items() if not k.startswith('_')}
        del data['id']
        data['url']='%s#should_not_go_in%s' % (data['url'],ts)
        data['created_on']=datetime.now()
        data['source_type']=4
        data['city']=u'成都'
        alive_item=UsedCar(**data)
        session.add(alive_item)

        session.commit()
        return [expired_item, alive_item]

    @classmethod
    def mark_duplicate(cls, session, item_id, old_item_ids=None):
        '''
        去重接口会调用这里，忽略即可
        '''
        pass

class ReasonTrack(Base):
    __tablename__ = 'open_clean_track'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, default=0, doc=u'编号')
    domain = Column(String(30), default='', doc=u'所在域')
    code = Column(String(20), nullable=True, doc=u'原因')
    detail = Column(String(512), doc=u'详情')
    ctx = Column(String(1024), doc=u'详情')
    created_at = Column(DateTime, doc=u'发生时间')
