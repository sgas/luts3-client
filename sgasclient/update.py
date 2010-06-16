"""
Functionality for update usage records between versions.
"""

import time

from twisted.python import log
from twisted.internet import defer

from sgasclient import couchdb



JAVASCRIPT_GET_CONVERT_VERSION = """
function(doc) {

  if (!doc.convert_version) {
    emit(null, 1);
  }
  else {
    emit(null, doc.convert_version);
  }

}
"""

JSON_DATETIME_FORMAT = "%Y %m %d %H:%M:%S"


# ur field names
START_TIME  = 'start_time'
END_TIME    = 'end_time'
SUBMIT_TIME = 'submit_time'
CREATE_TIME = 'create_time'
INSERT_TIME = 'insert_time'
CONVERT_VERSION = 'convert_version'



def getDocumentVersions(db_url):

    def mapIdVersions(data):
        idvermap = {}
        for row in data['rows']:
            idvermap[str(row['id'])] = row['value']
        return idvermap

    def countVersions(idvermap):
        d = {}
        for id_, version in idvermap.items():
            d[version] = d.get(version, 0) + 1
        for version in sorted(d.keys()):
            log.msg("For version %i : %s documents." % (version, d[version]))
        return idvermap

    db = couchdb.Database(db_url)
    d = db.temporaryView(JAVASCRIPT_GET_CONVERT_VERSION)
    d.addCallback(mapIdVersions)
    d.addCallback(countVersions)
    return d


@defer.inlineCallbacks
def updateDocuments(db_url, idvermap):
    log.msg('Starting fetch-update-save cycle')

    db = couchdb.Database(db_url)

    for id, version in idvermap.items():
        if not version in VERSION_UPDATERS:
            log.msg('Document %s: No update to perform' % id)
            continue

        doc = yield db.retrieveDocument(id)
        # default to 1 if version does not exists (also done a few times in the next)
        assert doc.get(CONVERT_VERSION,1) == version, 'Document version mismatch for %s' % id

        while doc.get(CONVERT_VERSION,1) in VERSION_UPDATERS:
            log.msg('Document %s: Updating from version %i' % (id, doc.get(CONVERT_VERSION,1)))
            doc = VERSION_UPDATERS[doc.get(CONVERT_VERSION,1)](doc)

        res = yield db.insertDocuments([doc])

        log.msg('Document %s: Updating done' % id)



def convertISODateToJS(iso_date):
    # assumes a date of the format "2009-10-19T11:05:19Z"
    # .translate doesn't work properly on unicode strings,
    # so this is done the silly way
    js_date = iso_date.replace('-',' ').replace('T',' ').replace('Z','')
    return js_date



def updateVersion1To2(doc):
    # updates:
    # A: change date format from ISO to JS compatable for
    #    the fields: 'start_time', 'end_time', 'submit_time'
    # B: Add a convert_version field (set to 2) to the doc

    # version 1 of documents had no convert_version field
    assert CONVERT_VERSION not in doc, 'Wrong document version to convert'

    doc[START_TIME]  = convertISODateToJS(doc[START_TIME])
    doc[END_TIME]    = convertISODateToJS(doc[END_TIME])
    doc[SUBMIT_TIME] = convertISODateToJS(doc[SUBMIT_TIME])

    doc[CONVERT_VERSION] = 2

    return doc


def updateVersion2To3(doc):
    # update:
    # A: change date format from ISO to JS compatable
    #    for the fields: 'create_time'
    # B: add a field named 'insert_time' which the value
    #    of the current time in JS format if non-existing
    # C: bump version version 3

    assert doc[CONVERT_VERSION] == 2, 'Wrong document version to convert'

    doc[CREATE_TIME] = convertISODateToJS(doc[CREATE_TIME])

    if not INSERT_TIME in doc:
        doc[INSERT_TIME] = time.strftime(JSON_DATETIME_FORMAT, time.gmtime())

    doc[CONVERT_VERSION] = 3

    return doc



# this has to be defined after the update functions
VERSION_UPDATERS = {
    1 : updateVersion1To2,
    2 : updateVersion2To3
}

