# coding: utf-8
from __future__ import absolute_import

import os
import daemon
import lockfile
import tornado.ioloop
import tornado.web
import tornado.auth

from conf.settings import confs
from db.sessions import sessions


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('get /filo/{resource}/{username}/{sessionkey} ; return: 200 allowed, 403 denied')


class LockHandler(tornado.web.RequestHandler):
    def get(self, resource, username, sessionkey):
        current_sessionkey = sessions.get_session(username)
        if current_sessionkey:
            if current_sessionkey == sessionkey:
                sessions.renew_session(username)
                self.write('200 allowed - session renewed\n')
            else:
                self.set_status(403)
                self.write('403 denied - current: %s\n' % current_sessionkey)
        else:
            sessions.set_session(username, sessionkey)
            self.write('200 allowed - new session\n')


def start():
    application = tornado.web.Application([
            (r'/', HomeHandler),
            (r'/filo/([a-zA-Z]{3,20})/([a-zA-Z]{3,20})/([a-zA-Z]{3,20})/?', LockHandler),
        ], **{
            'static_path': os.path.join('static'),
            'template_path': os.path.join('templates'),
            'debug': confs.debug,
            'cookie_secret': confs.cookie_secret
    })
    application.listen(confs.port)
    print(' => Listening on %d' % confs.port)
    tornado.ioloop.IOLoop.instance().start()


def start_daemon():
    context = daemon.DaemonContext(working_directory='.', detach_process=True,
        pidfile=lockfile.FileLock(confs.pidfile))

    with context:
        start()
