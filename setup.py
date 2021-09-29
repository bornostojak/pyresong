#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['mutagen>=0.4.0']

setup(
    author="Borno Stojak",
    author_email='borno.stojak@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A radio automation software package for python",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyresong',
    name='pyresong',
    packages=find_packages(include=['pyresong', 'pyresong.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bornostojak/pyresong',
    version='0.0.2',
    zip_safe=False,
)
