#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-ucamprojectlight',
    description='A Django module to use the template system of the University of Cambridge: Project light',
    long_description=open('README.rst').read(),
    url='https://git.csx.cam.ac.uk/x/ucs/raven/django-ucamprojectlight.git',
    version='1.1',
    license='MIT',
    author='Information Systems Group, University Information Services, University of Cambridge',
    author_email='information-systems@ucs.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
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
