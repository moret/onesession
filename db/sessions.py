from redis import StrictRedis


class Sessions(object):
    def _get_connection(self):
        return StrictRedis()

    r = property(_get_connection)

    def set_session(self, username, sessionkey):
        return self.r.setex(username, 60, sessionkey)

    def renew_session(self, username):
        return self.r.expire(username, 60)

    def get_session(self, username):
        return self.r.get(username)

sessions = Sessions()
