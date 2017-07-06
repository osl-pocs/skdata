#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'IPython',
    'jupyter',
    'ipywidgets',
    'matplotlib',
    'pandas',
    'numpy'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='scikit-data',
    version='0.1.0',
    description="The propose of this library/plugin is to allow the data analysis process more easy and automatic.",
    long_description=readme + '\n\n' + history,
    author="Ivan Ogasawara",
    author_email='ivan.ogasawara@gmail.com',
    url='https://github.com/OpenDataScienceLab/skdata',
    download_url = 'https://github.com/OpenDataScienceLab/skdata/archive/master.tar.gz',
    packages=[
        'skdata',
    ],
    package_dir={'skdata':
                 'skdata'},
    entry_points={
        'console_scripts': [
            'skdata=skdata.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='PyDataAnalysis',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
