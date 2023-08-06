#!/usr/bin/env python

import os.path
from setuptools import find_packages, setup

setup(
	name             = 'technic-solder-client',
	version          = '1.0',
	description      = 'Python implementation of a Technic Solder client',
	author           = 'Cadyyan',
	author_email     = 'cadyyan@gmail.com',
	url              = 'https://github.com/cadyyan/technic-solder-client',
	license          = 'MIT',
	packages         = find_packages(),
	install_requires = [
		'colorama',
		'requests',
		'tabulate',
	],
	scripts          = [
		os.path.join('bin', 'solder'),
		os.path.join('bin', 'solder.py'),
	],
)

