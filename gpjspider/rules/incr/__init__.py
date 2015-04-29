# -*- coding: utf-8 -*-
import copy


def make_incr_rule(full_rule, start_urls):
    rule = copy.deepcopy(full_rule)

    if start_urls:
        rule['start_urls'] += start_urls

    rule['parse'].pop('next_page_url')
    return rule
