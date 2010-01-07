from distutils.core import setup

setup(name='sgas-luts3-client',
      version='0.0.2',
      description='SGAS LUTS3 Client',
      author='Henrik Thostrup Jensen',
      author_email='htj@ndgf.org',
      url='http://www.sgas.se/',
      packages=['sgas', 'sgas/client'],
      scripts=['sgas-ur-register', 'sgas-ur-update']

)

