#!/usr/bin/env python
'''
Created on 18-12-2012

@author: maciag.artur
'''
from setuptools import setup, find_packages

setup(
    name='wykop-sdk',
    version='0.1.1',
    description='Client library for Wykop API',
    
    long_description=open("README.rst").read(),
    author='Artur Maciag',
    author_email='maciag.artur@gmail.com',
    url='https://github.com/p1c2u/wykop-sdk',
    license='BSD',
    py_modules=[
        'wykop',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
