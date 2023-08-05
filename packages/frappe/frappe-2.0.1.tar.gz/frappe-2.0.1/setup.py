#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

__author__ = "joaonrb"

try:
    import testfm
except ImportError:
    raise LookupError("You must have test.fm >= 1.0.4 installed before (https://github.com/grafos-ml/frappe)")

import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="frappe",
    version="2.0.1",
    description="Frappe recommendation system backend.",
    author="Linas Baltrunas",
    author_email="linas@tid.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.txt"],
    },
    scripts = ["scripts/sb"],
    license="copyright.txt",
    include_package_data=True,
    install_requires=[
        "django==1.6.7",
        "pymysql",
        "django-cors-headers",
        "python-memcached",
        "djangorestframework",
        "docopt",
        "click"
    ],
    long_description=README,
    url = "https://github.com/grafos-ml/frappe",
    download_url = "https://github.com/grafos-ml/frappe/archive/v2.0.tar.gz",
    keywords = ["recommendation"],
)