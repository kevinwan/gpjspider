# -*- coding: utf-8 -*-
"""
测试用

从open_product_source\car_source\car_detailinfo\car_images删除一条记录
"""
import sys
sys.path.insert(0, '../')

from gpjspider.models.usedcars import UsedCar
from gpjspider.models.product import CarSource, CarDetailInfo, CarImage
from gpjspider.utils import get_mysql_connect

print sys.argv
if len(sys.argv) < 2:
    print(u'请输入要删除的 URL 的绝对路径')
    exit(1)
url = sys.argv[1]


Session = get_mysql_connect()
session = Session()

a = session.query(UsedCar).filter(UsedCar.url == url).first()
if not a:
    print("URL {0} is not in open_product_source".format(url))
    exit(1)
print("URL {0}'s id is {1}".format(url, a.id))
session.delete(a)
b = session.query(CarSource).filter(CarSource.url == a.url).first()
session.delete(b)
session.query(CarDetailInfo).filter(CarDetailInfo.car_id == a.id).delete()
session.query(CarImage).filter(CarImage.car_id == a.id).delete()
try:
    session.commit()
except:
    session.rollback()
    print(u'删除失败，还原')
else:
    print(u"删除成功")
