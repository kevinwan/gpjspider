# -*- coding: utf-8 -*-
from fabric.api import *

env.user = 'gpjspider'
env.password = 'Sw21qazX'
env.port = 22000


class Host:
    _all = []

    def __init__(self):
        env.hosts = self._all


@task
class Aliyun(Host):
    crawler_1 = '123.57.207.123:22'
    crawler_2 = '123.57.210.155:22'
    _all = [crawler_1, crawler_2]


@task
class West(Host):
    crawler_1 = '211.149.190.122'
    crawler_2 = '211.149.169.237'
    _all = [crawler_1, crawler_2]

env.hosts = ['localhost']


@task
class Crawlers(Host):
    # _c1, _c2 = _all = West._all
    # _c3 = Aliyun.crawler_1
    _c1, _c2 = _all = '211.149.190.122 211.149.169.237'.split()
    _c3, _c4 = aliyun = '123.57.207.123:22 123.57.210.155:22'.split()
    _all.extend(aliyun)


class Crawler:
    crawler = 'localhost'
    crawler = None

    def __init__(self):
        env.hosts = [self.crawler]


@task
class C1(Crawler):
    crawler = Crawlers._c1


@task
class C2(Crawler):
    crawler = Crawlers._c2


@task
class C3(Crawler):
    crawler = Crawlers._c3


@task
class C4(Crawler):
    crawler = Crawlers._c4


class Server:
    WEST = 'west'
    ALI = 'aliyun'

ROLES = env.roledefs = {
    Server.WEST: West._all,
    Server.ALI: Aliyun._all,
}


class Path:
    pass


class Dir(Path):
    spider_repo = '/home/gpjspider/projects/gpjspider'


@task
def ping():
    with hide('running'):
        # with show('running'):
        run('echo "%(user)s"' % env)


from fabric.api import local


def commit():
    local("git add -p && git commit")


# def push():
#     local("git push")


# def prepare_deploy():
#     test()
#     commit()
#     push()


@task
def sync_spider():
    rsync_project
    with prefix('workon gpj'):
        pass


@task
def deploy(debug=True):
    with cd(Dir.spider_repo):
        update = 'git pull'
        if debug:
            has_diff = run('git diff | wc -l')
            if int(has_diff):
                run('git diff')
                ans = prompt('need stash, s/c/q?')
                if ans == 's':
                    update = 'git stash; %s; git stash pop' % update
                elif ans == 'c':
                    update = 'git checkout . && git pull'
                elif ans == 'q':
                    return
        else:
            update = 'git checkout .; git pull'
        # run('git status')
        run(update)
        run('find . -name "*.pyc" -exec rm -rf {} \;')
        # run('make clean')


@task
def nose():
    local('nosetests')
