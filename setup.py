# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

long_desc = '''
This package contains the adadomain Sphinx extension.

'''

requires = ['Sphinx>=1.4']

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sphinxcontrib-adadomain',
    version='0.2',
    url='http://bitbucket.org/tkoskine/sphinxcontrib-adadomain',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-adadomain',
    license='BSD',
    author='Tero Koskinen',
    author_email='tero.koskinen@iki.fi',
    description='Sphinx "adadomain" extension',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
