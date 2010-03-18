from distutils.core import setup

setup(name='sgas-luts-client',
      version='3.1.0-svn',
      description='SGAS LUTS Client',
      author='Henrik Thostrup Jensen',
      author_email='htj@ndgf.org',
      url='http://www.sgas.se/',
      packages=['sgas', 'sgas/client'],
      scripts=['sgas-ur-register', 'sgas-ur-update']

)

