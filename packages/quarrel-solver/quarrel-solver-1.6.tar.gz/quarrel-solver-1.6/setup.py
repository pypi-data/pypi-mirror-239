version = '1.6'

from setuptools import setup

setup(
	name='quarrel-solver',
	version=version,
	description='Tool for Quarrel (video game)',
	long_description=open('README.md', 'r').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/silvncr/quarrel',
	author='silvncr',
	include_package_data=True,
	license='MIT',
	packages=['quarrel_solver'],
	setup_requires=['pytest_runner'],
	python_requires='>=3.6',
	scripts=[],
	tests_require=['pytest'],
	entry_points={},
	zip_safe=True,
	classifiers=[
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Games/Entertainment :: Board Games',
		'Topic :: Games/Entertainment :: Puzzle Games',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)
