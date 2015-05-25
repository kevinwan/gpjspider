# -*- coding: utf-8 -*-
from gpjspider.tasks.spiders import *
from gpjspider.tasks.clean.usedcars import clean_domain


def main(name='test', type_='incr'):
    if name == '.':
        return clean_domain()
    # elif name.endswith('.com'):
    #     clean_domain(name)
    else:
        try:
            eval('run_%s_spider' % type_)(name)
        except:
            run_spider('%s.%s' % (type_, name))

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:3])
