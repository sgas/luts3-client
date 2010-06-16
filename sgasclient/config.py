"""
config module for sgas luts client.

Author: Henrik Thostrup Jensen <htj@ndgf.org>
Copyright: Nordic Data Grid Facility (2009)
"""

from twisted.python import usage



# configuration defaults
DEFAULT_HOSTKEY      = '/etc/grid-security/hostkey.pem'
DEFAULT_HOSTCERT     = '/etc/grid-security/hostcert.pem'
DEFAULT_CERTDIR      = '/etc/grid-security/certificates'


class ConfigurationError(Exception):
    pass


class CertificateOptions(usage.Options):

    optParameters = [ ['key',   'k', DEFAULT_HOSTKEY,  'Certificate key to use' ],
                      ['cert',  'c', DEFAULT_HOSTCERT, 'Certificate to use'     ],
                      ['cadir', 'd', DEFAULT_CERTDIR,  'Certificate directory'  ],
                    ]


class URRegistrationOptions(CertificateOptions):

    def parseArgs(self, *args):
        if len(args) in (0,1):
            raise usage.UsageError('Not enough arguments specified (url file1 ...)')
        self['url'] = args[0]
        self['urfiles'] = args[1:]


class URUpdateOptions(usage.Options):

    def parseArgs(self, *args):
        if len(args) != 1:
            raise usage.UsageError('UR update requires one (and only one argument)')
        self['url'] = args[0]

