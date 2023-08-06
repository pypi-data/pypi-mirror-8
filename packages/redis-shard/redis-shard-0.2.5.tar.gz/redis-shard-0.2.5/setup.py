#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os
import redis_shard


def read_file(*path):
    base_dir = os.path.dirname(__file__)
    file_path = (base_dir, ) + tuple(path)
    return open(os.path.join(*file_path)).read()

setup(
    name="redis-shard",
    url="http://blog.flyzen.com",
    license="BSD",
    author="Young King",
    author_email="yanckin@gmail.com",
    description="Redis Sharding API",
    long_description=(
        read_file("README.rst") + "\n\n" +
        "Change History\n" +
        "==============\n\n" +
        read_file("CHANGES.rst")),
    version=redis_shard.__version__,
    packages=["redis_shard"],
    include_package_data=True,
    zip_safe=False,
    install_requires=['redis', ],
    tests_require=['Nose'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
