#!/usr/bin/env python
#import sys
from distutils.core import setup

# if sys.version < '2.5':
#     sys.exit('Python 2.5 or higher is required')

setup(name='pysectools',
      version='0.2.0',
      description="""Various security-related functions""",
#      long_description="""""",
      license='WTFPL',
      author='Greg V',
      author_email='greg@unrelenting.technology',
      url='https://github.com/myfreeweb/pysectools',
      packages=['pysectools'],
      keywords=['security', 'pinentry', 'getpass', 'capsicum'],
      classifiers=[
          'Operating System :: POSIX',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'License :: Public Domain',
          'Topic :: Security'
      ],
      package_data={})
