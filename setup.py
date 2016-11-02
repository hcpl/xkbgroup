#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from xkbgroup.version import VERSION


setup(
    name="xkbgroup",
    version=VERSION,
    description="Query and change XKB layout state",
    author="Nguyen Duc My",
    author_email="hcpl.prog@gmail.com",
    url="https://github.com/hcpl/xkbgroup",
    packages=["xkbgroup"],
    package_data={"": ["LICENSE"]},
    license="MIT",
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Desktop Environment :: Window Managers",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        "console_scripts": [
            "xkbgroup = xkbgroup.__main__:main"
        ]
    },
)
