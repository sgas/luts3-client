"""
Various utility functionality that doesn't belong anywhere else.
"""

import sys
import time

from twisted.python import log, usage
from twisted.internet import reactor, defer


TIME_FORMAT = '%H:%M:%S'


def logObserver(eventDict):

    timestamp = time.strftime(TIME_FORMAT)
    text = '[' + timestamp + '] ' + log.textFromEventDict(eventDict)
    if eventDict['isError']:
        sys.stderr.write(text + '\n')
    else:
        sys.stdout.write(text + '\n')



def wrapMain(func):
    """
    Wrap a main function for proper twisted encapsulation and
    getting proper error feedback on the command line.
    """
    def handleError(error):
        if error.type == SystemExit:
            log.msg('SystemExit: %s' % error.value)
        elif error.type == usage.UsageError:
            log.msg(error.value)
        else:
            error.printTraceback()

    log.startLoggingWithObserver(logObserver, setStdout=0)

    d = defer.maybeDeferred(func)
    d.addErrback(handleError)
    d.addBoth(lambda _ : reactor.stop())
    return d

