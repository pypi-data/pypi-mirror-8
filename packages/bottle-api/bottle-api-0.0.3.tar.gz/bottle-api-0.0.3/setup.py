#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='bottle-api',
    version='0.0.3',
    description='useful decorator for building WebAPI on Bottle web framework development',
    author='Tomotaka Ito',
    author_email='tomotaka.ito@gmail.com',
    url='https://github.com/tomotaka/bottle-api',
    packages=find_packages(),
    license=open('LICENSE').read(),
    include_package_data=True,
    install_requires=[
    	'bottle'
    ],
    tests_require=['nose', 'WebTest'],
    test_suite='nose.collector'
)
