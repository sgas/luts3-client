import time

from distutils.core import setup

from sgasclient import __version__

setup(name='sgas-luts-client',
      version=__version__,
      description='SGAS LUTS Client',
      author='Henrik Thostrup Jensen',
      author_email='htj@ndgf.org',
      url='http://www.sgas.se/',
      packages=['sgasclient'],
      scripts=['sgas-ur-register', 'sgas-ur-update', 'sgas-db-migrate', 'sgas-postgres-migrate']
)

