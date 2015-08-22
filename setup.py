from setuptools import setup

__author__ = 'Denis'
__version__ = (0, 3, 2)

setup(name='Flask-Composer',
      version='.'.join(str(i) for i in __version__),
      description='Composite Web UI extension for Flask',
      long_description=open('README.md').read(),
      license='Apache 2.0',
      author='Denis Itskovich',
      author_email='denis.itskovich@gmail.com',
      url='https://github.com/denis-itskovich/flask-composer',
      packages=['flask_composer'],
      keywords=['flask', 'composite', 'web', 'flask-composer'],
      install_requires=['Flask'],
      tests_require=['Flask-Mako', 'nose'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Environment :: Web Environment',
                   'Framework :: Flask',
                   'License :: OSI Approved :: Apache Software License'
                   ],
      test_suite='nose.collector',
      )
