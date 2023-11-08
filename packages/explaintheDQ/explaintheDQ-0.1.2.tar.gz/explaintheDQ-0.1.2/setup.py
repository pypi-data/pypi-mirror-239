#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['astropy']

test_requirements = ['pytest>=3', ]

setup(
    author="Everett Schlawin",
    author_email='granfalloontoyballoon@hotmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="explains the JWST DQ value",
    entry_points={
        'console_scripts': [
            'explaintheDQ=explaintheDQ.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='explaintheDQ',
    name='explaintheDQ',
    packages=find_packages(include=['explaintheDQ', 'explaintheDQ.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/eas342/explaintheDQ',
    version='0.1.2',
    zip_safe=False,
)
