#-*- coding:utf-8 -*-
from setuptools import setup
import sys, os

version = '0.4'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
AUTHORS = open(os.path.join(here, 'AUTHORS.rst')).read()

# hack, or test wont run on py2.7
try:
    import multiprocessing
    import logging
except:
    pass

setup(name='wsgicors',
      version=version,
      description="WSGI for Cross Origin Resource Sharing (CORS)",
      long_description=README + '\n\n' +  CHANGES + '\n\n' +  AUTHORS,
      classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: WSGI"
        ],
      keywords=["wsgi", "cors"],
      author='Norman Krämer',
      author_email='kraemer.norman@googlemail.com',
      url="https://github.com/may-day/wsgicors",
      license='Apache Software License 2.0',
      py_modules=["wsgicors"],
      tests_require = [
        'nose',
        'nose-testconfig',
        'webob'
        ],
      test_suite = 'nose.collector',
      entry_points = """
      [paste.filter_app_factory]
      middleware = wsgicors:make_middleware
      """
      )
