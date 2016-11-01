#! /usr/bin/env python

from setuptools import setup


setup(
    name="xkbgroup",
    version="0.1",
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
)
