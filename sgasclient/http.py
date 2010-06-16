"""
http module for the sgas client.

Author: Henrik Thostrup Jensen <htj@ndgf.org>
Copyright: Nordic Data Grid Facility (2009)
"""

from twisted.internet import reactor
from twisted.python import log
from twisted.web import client



def httpRequest(url, method='GET', payload=None, ctxFactory=None):
    # probably need a header options as well
    """
    Peform a http request.
    """
    # copied from twisted.web.client in order to get access to the
    # factory (which contains response codes, headers, etc)

    scheme, host, port, path = client._parse(url)
    factory = client.HTTPClientFactory(url, method=method, postdata=payload)
    factory.noisy = False # stop spewing about factory start/stop
    # fix missing port in header (bug in twisted.web.client)
    if port:
        factory.headers['host'] = host + ':' + str(port)

    if scheme == 'https':
        reactor.connectSSL(host, port, factory, ctxFactory)
    else:
        reactor.connectTCP(host, port, factory)

    return factory.deferred, factory



def insertUsageRecords(url, payload, ctxFactory=None):
    """
    Register (upload/insert) one or more usage record in a usage record service.
    """
    def gotResponse(result, factory, url):
        if factory.status != '200':
            log.msg("Reply from %s had other response code than 200 (%s)" % (url, factory.status))
        return result

    d, f = httpRequest(url, method='POST', payload=payload, ctxFactory=ctxFactory)
    d.addCallback(gotResponse, f, url)
    return d

