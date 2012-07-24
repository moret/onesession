# coding: utf-8
from __future__ import absolute_import

import sys
sys.path = ['.'] + sys.path

from paver.easy import task
from paver.easy import consume_args
from paver.easy import sh


@task
def tests():
    clean()
    import pytest
    import coverage
    cov = coverage.coverage(omit='lib/*')
    cov.erase()
    cov.start()
    import conf.settings
    print 'setting environment to tests...'
    conf.settings.confs = conf.settings.tests
    pytest.main('-s -v tests')
    cov.stop()
    cov.report()
    clean()


@task
@consume_args
def run(args):
    clean()
    import conf.settings
    if 'prod' in args:
        print 'setting environment to prod!'
        conf.settings.confs = conf.settings.prod
    from web import server
    server.start()
    clean()


@task
@consume_args
def start(args):
    clean()
    import conf.settings
    if 'prod' in args:
        print 'setting environment to prod!'
        conf.settings.confs = conf.settings.prod
    from web import server
    server.start_daemon()
    clean()


@task
def stop():
    clean()
    import conf.settings
    sh("ps aux | egrep '%s/bin/paver' | awk '{print $2}' | xargs kill -9;" % conf.settings.confs.appname)
    sh('rm %s.lock' % conf.settings.confs.pidfile)
    clean()


@task
def clean():
    sh('find . -name "__pycache__" -delete')
    sh('find . -name "*.pyc" -delete')
    sh('find . -name "*~" -delete')
