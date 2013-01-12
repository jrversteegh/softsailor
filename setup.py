#!/usr/bin/env python

"""
setup.py file for installing module
"""

from distutils.core import setup, Extension

setup (
    name = 'softsailor',
    version = '0.1',
    author = "J.R. Versteegh",
    author_email = "<j.r.versteegh@gmail.com>",
    description = """Module for sailing calculations, simulation and routing""",
    packages = ['softsailor', 'softsailor.sol', 'softsailor.grb'],
)

