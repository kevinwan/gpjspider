# -*- coding: utf-8 -*-
from gpjspider.models.product import City
from gpjspider.utils import get_mysql_connect


Session = get_mysql_connect()


def get_gongpingjia_city(city_name, domain):
    """
    """
    session = Session()
    q = session.query(City).filter(City.name == city_name)
    q = q.filter(City.parent is not None)
    return q.first()
