#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from gpjspider.utils import get_mysql_connect
session = get_mysql_connect()()
from gpjspider.utils import get_redis_cluster
redis = get_redis_cluster()
from gpjspider.utils.constants import (
    REDIS_DUP_SIG_KEY,
    REDIS_DUP_STAT_KEY,
    REDIS_DUP_CHECKED_KEY,
    REDIS_DUP_CACHE_OPEN_PRODUCT_SOURCE,
)


if 1:
    sqls=[]
    sqls.append('''
CREATE TABLE IF NOT EXISTS `tmp_sigs`(
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `cnt` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `detail` VARCHAR(255) NOT NULL,
  `sig` CHAR(32) NOT NULL,
  `src` ENUM('CarSource','TradeCar','UsedCar') NOT NULL DEFAULT 'CarSource',
  `id_list` TEXT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `sig` (`sig`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB      
    '''.strip())
    sqls.append('truncate table tmp_sigs')
    # 从 CarSource (car_source)加载摘要信息到临时表
    sqls.append('''
    insert into tmp_sigs(detail,sig,cnt,src,id_list)
      SELECT
          detail, md5(detail) as sig, COUNT(1) AS cnt,'CarSource' as src, group_concat(id) as id_list
      FROM(
          SELECT CONCAT_WS('#', brand_slug, model_slug, city, year, mile, price, phone) as detail,
              id
          FROM car_source
          WHERE pub_time<curdate()
      ) AS s1
      GROUP BY s1.detail
    '''.strip())
    step=100000
    min_id,max_id=map(int, session.execute('select min(id),max(id) from open_sell_car where created_on<curdate()').first())
    print min_id,max_id
    for i,x in enumerate(xrange(min_id, max_id+1, step)):
        print i,x
        if i>0:
            high=x
            sqls.append('''
                insert into tmp_sigs(detail,sig,cnt,src,id_list)
                SELECT
                    detail, md5(detail) as sig, COUNT(1) AS cnt,'TradeCar' as src, group_concat(id) as id_list
                FROM(
                  SELECT CONCAT_WS('#', brand, model, city, year, mile, list_price, phone) as detail,
                      id
                  FROM open_sell_car
                  WHERE id between {} and {}
                ) AS s1
                GROUP BY s1.detail
            '''.format(low, high).strip())
        low=x
    if REDIS_DUP_CACHE_OPEN_PRODUCT_SOURCE:
      step=100000
      min_id,max_id=map(int, session.execute('select min(id),max(id) from open_product_source where created_on<curdate()').first())
      print min_id,max_id
      for i,x in enumerate(xrange(min_id, max_id+1, step)):
          print i,x
          if i>0:
              high=x
              sqls.append('''
                  insert into tmp_sigs(detail,sig,cnt,src,id_list)
                  SELECT
                      detail, md5(detail) as sig, COUNT(1) AS cnt,'UsedCar' as src, group_concat(id) as id_list
                  FROM(
                    SELECT CONCAT_WS('#', brand_slug, model_slug, city, year, mile, price, phone) as detail,
                        id
                    FROM open_product_source
                    WHERE id between {} and {}
                  ) AS s1
                  GROUP BY s1.detail
              '''.format(low, high).strip())
          low=x
    for sql in sqls:
        print sql
        session.execute(sql)
if 1:
  min_id,max_id=map(int, session.execute('select min(id),max(id) from tmp_sigs where 1=1').first())
  for i,x in enumerate(xrange(min_id, max_id+1, 5000)):
          print i,x
          if i>0:
              high=x
              for sig,src,id_list in session.execute('select sig,src,id_list from tmp_sigs where id between %d and %d' % (low,high)):
                  pip=redis.pipeline()
                  rk = REDIS_DUP_SIG_KEY % sig
                  for _id in id_list.split(','):
                      item_id = '%s:%s' % (src, _id)
                      pip.sadd(REDIS_DUP_CHECKED_KEY, item_id)
                      pip.sadd(rk, item_id)
                      pip.zincrby(REDIS_DUP_STAT_KEY, sig)
                  pip.execute()
          low=x

print 'done'