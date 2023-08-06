#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import load_source
from distutils.core import setup

core = load_source("core", "w1thermsensor/__init__.py")

setup(
    name="w1thermsensor",
    version=core.__version__,
    license="GPLv2",
    description="This little pure python module provides a single class to get the temperature of a w1 sensor",
    author=core.__author__,
    author_email=core.__email__,
    maintainer=core.__author__,
    maintainer_email=core.__email__,
    platforms=["Linux"],
    url="http://github.com/timofurrer/w1thermsensor",
    download_url="http://github.com/timofurrer/w1thermsensor",
    packages=["w1thermsensor"]
)
