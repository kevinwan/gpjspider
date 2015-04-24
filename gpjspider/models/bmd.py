# -*- coding: utf-8 -*-
"""
品牌、型号、款型 模型
"""
from sqlalchemy import Column, Integer, String, Enum
# from sqlalchemy.orm import relationship
from . import Base


class BrandModel(Base):

    """
    车辆品牌、型号模型

    唯一性：
    - 品牌：name domain
    - 型号：name parent mum

    1)如果是品牌,那么只看名称,不考虑slug和url
    2)如果是型号,那么要看所属的品牌名称,型号自身名称,生产厂商这三个字段是否一样,都一样就是重复
      ,这条记录就不插入,不考虑slug和url.
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
    domain = Column(String(32), nullable=True)
    url = Column(String(500), default='', nullable=True)
    parent = Column(String(32), nullable=True)
    status = Column(Enum(STATUS_CHOICE), default='A')
    mum = Column(String(32), nullable=True, doc=u'生产车商', default=None)
    # source = Column("source_id", Integer, default=0)
