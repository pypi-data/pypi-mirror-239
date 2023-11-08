#!/usr/bin/env python3

import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(

	name='phixpy',
	version='0.0.2',
	description='A package for physics operation (currently only for vector operation)',
	long_description=long_description,
	long_description_content_type = 'text/markdown',
	author='Rijul Dhungana',
	author_email = 'rijuldhungana37@gmail.com',
	classifiers=
	[
		"Development Status :: 3 - Alpha" ,
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Topic :: Utilities"
	],
	python_requires = ">=3.7",
	install_requires=['numpy', 'matplotlib'],
	packages=setuptools.find_packages(),
	include_packages=True
	)
