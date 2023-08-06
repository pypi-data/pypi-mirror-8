#!/usr/bin/env python

from os.path import dirname

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

pwd = dirname(__file__)

setup(
    name="licenser",
    version="1.1.0",
    description="Quickly add an open-source license to your project.",
    author="Ty-Lucas Kelley",
    author_email="tylucaskelley@gmail.com",
    license="MIT",
    url="http://github.com/tylucaskelley/licenser",
    download_url="https://github.com/tylucaskelley/licenser/tarball/v1.1.0",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ],
    entry_points={
        "console_scripts": [
            "licenser=licenser:main"
        ]
    },
    packages=[
        "licenser"
    ],
    package_dir={
        "licenser": "licenser"
    },
    package_data={
        "licenser": [
            "licenses/*"
        ]
    },
    test_suite="tests"
)
