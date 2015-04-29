# -*- coding: utf-8 -*-
from gpjspider.tasks.spiders import *


def main(name='test', type_='full'):
    eval('run_%s_spider' % type_)(name)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:3])
