#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gpjspider.tasks.clean.usedcars import update_dup_cars,update_dup_car
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--step", default=500, help="每一步更新多少")
    parser.add_argument("-l", "--limit", default=0, help="是否只采样更新部分")
    parser.add_argument("-a", "--async", default=0, help="async update")
    parser.add_argument("-q", "--quick", default=0, help="quick update")
    parser.add_argument("-t", "--test", default=0, help="test")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    if int(args.test):
        from gpjspider.tasks.clean.usedcars import test_dup_car
        test_dup_car()
    elif int(args.quick):
        from gpjspider.tasks.clean.usedcars import update_dup_car
        from gpjspider.models.product import CarSource
        from gpjspider.utils import get_mysql_connect
        from gpjspider.utils import get_redis_cluster
        redis = get_redis_cluster()
        session = get_mysql_connect()()
        sql='''
        SELECT
            detail, COUNT(1) AS cnt,group_concat(id) as id_list
        FROM(
            SELECT CONCAT_WS('#', brand_slug, model_slug, city, year, mile, price, phone) as detail,
                id
            FROM car_source
            WHERE 1=1
            ORDER BY id DESC
            -- LIMIT 1000
        ) AS s1
        GROUP BY s1.detail
        HAVING cnt >1
        ORDER BY cnt DESC
        '''
        for row in session.execute(sql):
            for item_id in row[2].split(','):
                update_dup_car(CarSource.__name__, item_id)
        min_id = session.query(CarSource.id).order_by(CarSource.id.asc()).limit(1).scalar()
        max_id = session.query(CarSource.id).order_by(CarSource.id.desc()).limit(1).scalar()
        print 'car_source min_id: ', min_id, ' max_id: ', max_id
        for item_id in xrange(int(min_id), int(max_id)):
            print 'checking', item_id
            try:
                update_dup_car(CarSource.__name__, item_id)
            except Exception as e:
                if 'not exists' in e.message:
                    print e.message
                else:
                    raise
    else:
        update_dup_cars(int(args.step), int(args.limit), args.async)



