#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

requirements = [
    # see requirements.txt
    "sympy"
]

test_requirements = [
    # see requirements/test.txt
]

setup(
    name='datavalidation',
    version='1.0.0',
    description="A micro-service to perform data validation on bike geometries",
    long_description=readme + '\n\n' + history,
    author="Javier Chiyah Garcia, Mario Vasilev, Jamie McCulloch, Matthew Innes",
    author_email='{fjc3, mvv1, jm7, mci30}@hw.ac.uk',
    url='https://github.com/jchiyah/datavalidation',
    packages=[
        'datavalidation',
    ],
    package_dir={'datavalidation':
                 'datavalidation'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU Affero General Public License v3",
    zip_safe=False,
    keywords='datavalidation',
    classifiers=[
        'Development Status :: Beta Release',
        'Intended Audience :: Developers',
        'License :: GNU Affero General Public License v3 (AGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
