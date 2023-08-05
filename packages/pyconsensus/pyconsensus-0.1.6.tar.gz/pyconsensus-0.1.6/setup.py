#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="pyconsensus",
    version="0.1.6",
    description="Consensus mechanism for Truthcoin",
    author="Jack Peterson and Paul Sztorc",
    author_email="<jack@dyffy.com>",
    maintainer="Jack Peterson",
    maintainer_email="<jack@dyffy.com>",
    license="GPL",
    url="https://github.com/tensorjack/pyconsensus",
    download_url = "https://github.com/tensorjack/pyconsensus/tarball/0.1.6",
    packages=["pyconsensus"],
    install_requires=["numpy", "six"],
    keywords = ["consensus", "prediction market", "PM", "truthcoin", "oracle"]
)
