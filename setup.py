import time

from distutils.core import setup

gmt = time.gmtime()
day = '%04d%02d%02d' % (gmt.tm_year, gmt.tm_mon, gmt.tm_mday)

version='3-svn-%s' % day

setup(name='sgas-luts-client',
      version=version,
      description='SGAS LUTS Client',
      author='Henrik Thostrup Jensen',
      author_email='htj@ndgf.org',
      url='http://www.sgas.se/',
      packages=['sgasclient'],
      scripts=['sgas-ur-register', 'sgas-ur-update', 'sgas-db-migrate', 'sgas-postgres-migrate']
)

