#-*- coding:utf-8 -*-
def filter_item_ids(item_ids, klass_name):
    return [x[1] for x in [item_id.isdigit() and [klass_name, item_id] or item_id.split(':') for item_id in item_ids] if x[0]==klass_name]

def conver_item_ids(item_ids, target_klass_name):
    new_item_ids = []
    from collections import defaultdict
    klass_item_ids = defaultdict(list)
    for item_id in item_ids:
        if item_id.isdigit():
            new_item_ids.append(item_id)
        else:
            klass_name, klass_id = item_id.split(':')
            if klass_name==target_klass_name:
                new_item_ids.append(klass_id)
            else:
                klass_item_ids[klass_name].append(klass_id)
    if klass_item_ids:
        from gpjspider.utils import get_mysql_connect
        session = get_mysql_connect()()
        for klass_name,item_ids in klass_item_ids.iteritems():
            if klass_name=='UsedCar' and target_klass_name=='CarSource':
                for row in session.execute('select cs.id from open_product_source as ops left join  car_source as cs on cs.url=ops.url where ops.id in (%s)' % ','.join(item_ids)):
                    new_item_ids.append(row[0])
            elif klass_name=='UsedCar' and target_klass_name=='TradeCar':
                for row in session.execute('select osc.id from open_sell_car as osc where osc.car_id in (%s)' % ','.join(item_ids)):
                    new_item_ids.append(row[0])
            else:
                pass
        session.close()
    return new_item_ids

def sorted_unique_list(l):
    return reduce(lambda x,y: y[0] in x and x or x+y, [[xs] for xs in l])

import time
import datetime

def timing_call(stat_file):
    def dec(func):
        def wraped_func(*args, **kwargs):
            b1=time.time()
            func(*args, **kwargs)
            b2=time.time()
            with open(stat_file, 'a') as f:
                f.write("%s %s %s\n" % (datetime.datetime.fromtimestamp(b1), datetime.datetime.fromtimestamp(b2), b2-b1))
        return wraped_func
    return dec
