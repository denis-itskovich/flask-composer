__author__ = 'Denis'

from distutils.core import setup
from flask_composer import __version__

setup(name='Flask-Composer',
      version='.'.join(str(i) for i in __version__),
      description='Composite Web UI extension for Flask',
      long_description=open('README.md').read(),
      license='Apache 2.0',
      author='Denis Itskovich',
      author_email='denis.itskovich@gmail.com',
      url='https://github.com/denis-itskovich/flask-composer',
      packages=['flask_composer'],
      keywords=['flask', 'composite', 'web'],
      install_requires=['Flask'],
      test_requires=['Flask-Mako'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Environment :: Web Environment',
                   'Framework :: Flask',
                   'License :: OSI Approved :: Apache Software License'
                   ],
      )
