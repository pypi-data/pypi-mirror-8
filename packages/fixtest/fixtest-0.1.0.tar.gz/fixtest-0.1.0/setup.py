
import os

from setuptools import setup, find_packages

setup(
	name='fixtest',
	version='0.1.0',
	packages=find_packages(),
	install_requires=['twisted>=14.0.0'],
	license='MIT',
	author='Kenn Takara',
	author_email='kenn.takara@outlook.com',
	entry_points={
		'console_scripts': ['fixtest=fixtest.base.runner:main'],
	},
	classifiers={
        'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Financial and Insurance Industry',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.7',
		'Topic :: System :: Networking',
		'Topic :: Software Development :: Testing',
	},
	url='https://github.com/kennt/fixtest',
    description='Tool for testing FIX (Financial Information eXchange protocol) services',
)
