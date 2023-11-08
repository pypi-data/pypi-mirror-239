#!/usr/bin/env python3

import setuptools


LONG_DESCR = """

phixpy is a Python package that provides functions for physics operations.
With objects like 'vector' and 'matrix' user can perform the operations like
additions, subtraction, dot product etc.


"""

setuptools.setup(

	name='phixpy',
	version='0.0.1',
	description='A package for physics operation (currently only for vector operation)',
	long_description=LONG_DESCR,
	author='Rijul Dhungana',
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
