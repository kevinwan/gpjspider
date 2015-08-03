# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from gpjspider.tasks.clean.usedcars import *


def update_extra_cs(ids):
    for cid in ids:
        session = Session()
        cs = session.query(CarSource).get(cid)
        detail = cs.car_detail
        if not detail:
            print cid, 'no detail info'
            session.close()
            continue
        cs.qs_tags = get_qs_tags(detail.quality_assurance)
        item = {}
        for attr in 'id brand_slug model_slug model_detail_slug \
        mile year month city price volume color source_type'.split():
            item[attr] = getattr(cs, attr, '')
        eval_price = get_eval_price(item)
        if eval_price:
            gpj_index = get_gpj_index(item['price'], eval_price)
            add_extra_cols(cs, gpj_index, eval_price)
        # print cid, cs.qs_tags, cs.eval_price, cs.gpj_index
        session.add(cs)
        session.commit()
        session.close()


if __name__ == '__main__':
    end_date = start_date = datetime.today()
    start_date -= timedelta(weeks=1)
    end_date -= timedelta(days=1)
    # start_date -= timedelta(weeks=2)
    # end_date -= timedelta(weeks=1)
    # start_date -= timedelta(weeks=3)
    # start_date -= timedelta(weeks=8)
    # end_date -= timedelta(weeks=2)
    start_date = str(start_date)[:10]
    end_date = str(end_date)[:10]
    css = Session().query(CarSource.id).filter(CarSource.pub_time > start_date,
                                               CarSource.pub_time <= end_date,
                                               # CarSource.id >= 1403028,
                                               # CarSource.id <= 1382611,
                                               CarSource.qs_tags == None).order_by('-id')
    pool_run(css, update_extra_cs, cls=None)
