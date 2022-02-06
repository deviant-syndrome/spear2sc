# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('spear2sc/spear2sc.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cmdline-spear2sc",
    packages = ["spear2sc"],
    entry_points = {
        "console_scripts": ['spear2sc = spear2sc.spear2sc:main']
        },
    install_requires=[
        'numpy',
        'plotille',
        'publication',
        "supriya"
    ],
    version = version,
    description = "SPEAR2SC. SuperCollider-friendly Spear file reader.",
    long_description = long_descr,
    author = "Deviant Syndrome",
    url = "http://gehrcke.de/2014/02/distributing-a-python-command-line-application",
    )
