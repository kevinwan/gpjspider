#-*- coding:utf-8 -*-
def filter_item_ids(item_ids, klass_name):
    return [x[1] for x in [item_id.isdigit() and [klass_name, item_id] or item_id.split(':') for item_id in item_ids] if x[0]==klass_name]
