#!/bin/bash
#pkill celery
#sleep 10
ps aux|grep 'gpjspider.celery_app'|grep 'worker'|grep -v 'grep'|awk '{print $2}'|xargs kill -9
export DATE_SUFFIX=`date +'%Y%m%d%H%M%S'`
export DATE_SUFFIX=`date +'%Y%m%d'`
export ELERY_RDBSIG=1
export C_FORCE_ROOT=1 
cd ~/projects/gpjspider
for((i=1;i<=2;i++));
do
    ~/.virtualenvs/gpj/bin/celery worker -E -A gpjspider.celery_app -n celery_default${i} -Q default -O fair -l debug -f /tmp/gpjspider/celery-default-${DATE_SUFFIX}.${i}.log 2>&1 1>>/tmp/gpjspider/celery.error.log &
done
~/.virtualenvs/gpj/bin/celery worker -E -A gpjspider.celery_app -n celery_clean${i} -Q clean -O fair -l debug -f /tmp/gpjspider/celery-clean-${DATE_SUFFIX}.log 2>&1 1>>/tmp/gpjspider/celery.error.log &
#~/.virtualenvs/gpj/bin/celery flower -A gpjspider.celery_app --port=5678 2>&1 1>>/tmp/gpjspider/celery.flower.log &
