# -*- coding: utf-8 -*-
import imp
import sys
from os import path
from setuptools import setup, find_packages, Extension

info = imp.load_source('info', path.join('.', 'rider', 'info.py'))

NAME = info.NAME
DESCRIPTION = info.DESCRIPTION
AUTHOR = info.AUTHOR
AUTHOR_EMAIL = info.AUTHOR_EMAIL
URL = info.URL
VERSION = info.VERSION
REQUIRES = ['falcon>=0.2.0b1', 'jinja2', 'gevent']

if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    REQUIRES.append('importlib')

PYPY = True
CYTHON = False
try:
    sys.pypy_version_info
except AttributeError:
    PYPY = False

if not PYPY:
    try:
        from Cython.Distutils import build_ext
        CYTHON = True
    except ImportError:
        print('\nWARNING: Cython not installed. '
              'Rider will still work fine, but may run '
              'a bit slower.\n')
        CYTHON = False

if CYTHON:
    cmdclass = {'build_ext': build_ext}
    ext_modules = [
        Extension('rider.routes.urls', [path.join('rider/routes/', 'urls.py')]),
        Extension('rider.routes.__init__', [path.join('rider/routes/', '__init__.py')]),

        Extension('rider.views.response', [path.join('rider/views/', 'response.py')]),
        Extension('rider.views.decorators', [path.join('rider/views/', 'decorators.py')]),
        Extension('rider.views.exceptions', [path.join('rider/views/', 'exceptions.py')]),
        Extension('rider.views.__init__', [path.join('rider/views/', '__init__.py')]),

        Extension('rider.utils', [path.join('rider', 'utils.py')]),
        Extension('rider.http', [path.join('rider', 'http.py')]),
        Extension('rider.templates', [path.join('rider', 'templates.py')]),
    ]
else:
    cmdclass = {}
    ext_modules = []

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache 2.0",
    url=URL,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    scripts=['rider/bin/rider'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=REQUIRES,
    cmdclass=cmdclass,
    ext_modules=ext_modules
)
