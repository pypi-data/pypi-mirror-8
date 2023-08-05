#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def get(fname):
    try:
        with open(fname) as f:
            return f.read()
    except IOError:  # probably in tox
        return ''

setup(
    name='trek',
    version=get('VERSION'),
    description='generic migration provider',
    long_description=get('README.rst'),
    author='Brian Hicks',
    author_email='brian@brianthicks.com',
    url='https://github.com/brianhicks/trek',
    license=get('VERSION'),
    packages=find_packages(exclude=['tests']),

    entry_points={
        "console_scripts": [
            'trek = trek.cli:run'
        ]
    },
)
