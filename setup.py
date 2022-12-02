# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2022, Steven Masfaraud
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
Activity Watch Spyder plugin setup.
"""
from setuptools import find_packages
from setuptools import setup

from spyder_aw_watcher import __version__


setup(
    # See: https://setuptools.readthedocs.io/en/latest/setuptools.html
    name="spyder_aw_watcher",
    version=__version__,
    author="Steven Masfaraud",
    author_email="aw-spyder@masfaraud.fr",
    description="ActivityWatch watcher plugin for spyder",
    license="GNU General Public License v3",
    url="https://github.com/masfaraud/spyder_aw_watcher",
    python_requires='>= 3.7',
    install_requires=[
        "qtpy",
        "qtawesome",
        "spyder>=5.0.1",
        "aw-client"
    ],
    packages=find_packages(),
    entry_points={
        "spyder.plugins": [
            "spyder_aw_watcher = spyder_aw_watcher.spyder.plugin:ActivityWatchSpyderplugin"
        ],
    },
    classifiers=[
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
)
