#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


install_requires = [
    'github3.py>=0.9.3,<0.10',
    'ruamel.yaml>=0.15.19,<.0.16',
]


setup(
    name='issuecounter',
    version="0.0.1",
    description='Multi-container orchestration for Docker',
    url='https://github.com/shin-/github-issue-counter',
    author='Joffrey F (based on code by @MorrisJobke)',
    license='MIT License (MIT)',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={},
    tests_require=[],
    entry_points="""
    [console_scripts]
    issue_counter=issuecounter.main:main
    """,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
