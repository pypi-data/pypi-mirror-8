#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class Source(resource.BaseResource):

    ROOT = 'data/sources'
    PASSTHRU_FIELDS = ['name', 'config']

    def list(self, callback=None, errback=None):
        return self._make_request('GET', '%s' % (self.ROOT),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, sourceid, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s/%s' % (self.ROOT, sourceid),
                                  callback=callback,
                                  errback=errback)

    def create(self, name, sourcetype, callback=None, errback=None, **kwargs):
        body = {
            'name': name,
            'sourcetype': sourcetype
        }
        self._buildStdBody(body, kwargs)
        return self._make_request('PUT',
                                  '%s' % (self.ROOT),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, sourceid, callback=None, errback=None, **kwargs):
        body = {
            'id': sourceid
        }
        self._buildStdBody(body, kwargs)
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, id),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, sourceid, callback=None, errback=None):
        return self._make_request('DELETE',
                                  '%s/%s' % (self.ROOT, sourceid),
                                  callback=callback,
                                  errback=errback)

    def publish(self, sourceid, data, callback=None, errback=None):
        return self._make_request('POST',
                                  'feed/%s' % (sourceid),
                                  body=data,
                                  callback=callback,
                                  errback=errback)


class Feed(resource.BaseResource):

    ROOT = 'data/feeds'
    PASSTHRU_FIELDS = ['name', 'config', 'destinations']

    def list(self, sourceid, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s/%s' % (self.ROOT, sourceid),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, sourceid, feedid, callback=None, errback=None):
        return self._make_request('GET',
                                  '%s/%s/%s' % (self.ROOT, sourceid, feedid),
                                  callback=callback,
                                  errback=errback)

    def create(self, sourceid, name, config, callback=None, errback=None,
               **kwargs):
        body = {
            'name': name,
            'config': config,
        }
        self._buildStdBody(body, kwargs)
        return self._make_request('PUT',
                                  '%s/%s' % (self.ROOT, sourceid),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, sourceid, feedid, callback=None, errback=None, **kwargs):
        body = {
            'id': feedid
        }
        self._buildStdBody(body, kwargs)
        return self._make_request('POST',
                                  '%s/%s/%s' % (self.ROOT, sourceid, feedid),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, feedid, callback=None, errback=None):
        return self._make_request('DELETE',
                                  '%s/%s' % (self.ROOT, feedid),
                                  callback=callback,
                                  errback=errback)
