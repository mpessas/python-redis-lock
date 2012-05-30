# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='redislock',
    version = '0.1',
    description='Locks on top of redis.',
    author='Apostolis Bessas',
    author_email='mpessas@gmail.com',
    long_description = long_description,
    packages = ['redislock', ],
    test_suite = 'tests',
    install_requires=['distribute', 'redis']
)
