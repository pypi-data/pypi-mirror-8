#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="voevent-parse",
    version="0.7.0",
    packages=['voeventparse', 'voeventparse.tests', 'voeventparse.tests.resources'],
    package_data={'voeventparse':['tests/resources/*.xml']},
    description="Convenience routines for parsing and manipulation of "
                "VOEvent XML packets.",
    author="Tim Staley",
    author_email="timstaley337@gmail.com",
    url="https://github.com/timstaley/voevent-parse",
    install_requires=required,
    test_suite='voeventparse.tests'
)
