"""
High-level commands for the sgas client.
"""

import urlparse

from OpenSSL import SSL

from twisted.python import log

from sgas.client import config, http, ssl, ur, update



def registerUsageRecords(url, urfiles, key=None, cert=None, cadir=None):
    """
    Register usage records to the given URL.
    """
    if not urfiles: # no registration to perform
        log.msg("No usage records to register.")
        return

    log.msg("Registrations to perform: %i files" % len(urfiles))

    payload = ur.joinUsageRecordFiles(urfiles)
    #print payload

    up = urlparse.urlparse(url)
    if up.scheme == 'http':
        cf = None
        log.msg("Warning: Registering to a http (and not https) URL.")
    elif up.scheme == 'https':
        cf = ssl.ContextFactory(key, cert, cadir, True)
    else:
        raise config.ConfigurationError("Invalid URL or url scheme not supported")

    log.msg("Sending http request to insert usage records.")

    d = http.insertUsageRecords(url, payload, cf)
    return d


def updateUsageRecords(db_url):
    """
    Updates usage record in a CouchDB datebase, specified by the URL.
    """
    log.msg('This command will take some time if you have a high number of documents in CouchDB')
    log.msg('Fetching list of document versions')

    updateDoc = lambda idvermap : update.updateDocuments(db_url, idvermap)

    d = update.getDocumentVersions(db_url)
    d.addCallback(updateDoc)

    return d



