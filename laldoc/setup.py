#! /usr/bin/env python

"""Setup configuration file for laldoc."""

from setuptools import setup


# Run the setup tools
setup(
    name='laldoc',
    version='0.1-dev',
    author='AdaCore',
    author_email='support@adacore.com',
    url='https://www.adacore.com',
    description='Libadalang-based Ada source extractor for documentation',
    packages=['laldoc']
)
