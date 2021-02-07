# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in flutterwave/__init__.py
from flutterwave import __version__ as version

setup(
	name='flutterwave',
	version=version,
	description='Flutterwave integration for ERPNext',
	author='Babatunde Akinyanmi',
	author_email='tundebabzy@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
