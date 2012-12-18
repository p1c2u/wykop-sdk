#!/usr/bin/env python
'''
Created on 18-12-2012

@author: artur
'''
from setuptools import setup, find_packages

setup(
    name='wykop-sdk',
    version='0.1.0',
    description='Client library for Wykop API',
    
    long_description=open("README.rst").read(),
    author='Artur Maciag',
    author_email='maciag.artur@gmail.com',
    url='https://github.com/pythonforfacebook/facebook-sdk',
    license='Apache',
    packages=find_packages(exclude=('tests', 'example')),
    py_modules=[
        'wykop',
    ],
    test_suite='runtests.runtests',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
