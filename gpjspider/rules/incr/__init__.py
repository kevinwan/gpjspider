# -*- coding: utf-8 -*-
import copy


def make_incr_rule(full_rule, start_urls=[]):
    rule = copy.deepcopy(full_rule)
    # p = rule.get('parse_list', rule['parse'])
    for k in 'parse_list parse'.split():
        p = rule.get(k)
        if p and 'next_page_url' in p:
            incr = p['incr_page_url'] = p.pop('next_page_url')

    # incr['incr_pagenum'] = 3
    return rule
