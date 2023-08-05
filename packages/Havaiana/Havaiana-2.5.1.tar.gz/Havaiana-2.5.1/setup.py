#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Havaiana',
    version='2.5.1',
    author='Felipe Lerena',
    author_email='felipelerena@gmail.com',
    packages=['havaiana'],
    include_package_data=True,
    package_data={
        'havaiana/templates': ['*'],
    },
    scripts=[],
    url='http://pypi.python.org/pypi/Havaiana/',
    license='LICENSE.txt',
    description='A GUI for Ojota - Alows to edit, create and remove elements',
    long_description=open('README.txt').read(),
    install_requires=["ojota", "flask", "wtforms", "pygal", "flask-paginate"],
)
