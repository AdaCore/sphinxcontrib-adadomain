# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages

long_desc = '''
This package contains the adadomain Sphinx extension.

'''

requires = ['Sphinx>=1.0']

def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except IOError:
        pass

setup(
    name='sphinxcontrib-adadomain',
    version='0.2',
    url='http://bitbucket.org/tkoskine/sphinxcontrib-adadomain',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-adadomain',
    license='BSD',
    author='Tero Koskinen',
    author_email='tero.koskinen@iki.fi',
    description='Sphinx "adadomain" extension',
    long_description=readme(),
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
