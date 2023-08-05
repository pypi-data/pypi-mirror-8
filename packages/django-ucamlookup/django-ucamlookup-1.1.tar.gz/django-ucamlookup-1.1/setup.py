#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-ucamlookup',
    description='A Django module for the University of Cambridge Lookup service',
    long_description=open('README.rst').read(),
    url='https://git.csx.cam.ac.uk/x/ucs/u/amc203/django-ucamlookup.git',
    version='1.1',
    license='MIT',
    author='Information Systems Group, University Information Services, University of Cambridge',
    author_email='information-systems@ucs.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)