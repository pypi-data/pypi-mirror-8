#! /usr/bin/env python

from setuptools import setup

exec(open("./gedcom/_version.py").read())

setup(
    name='gedcompy',
    version=__version__,
    packages=['gedcom',],
    license='GPLv3+',
    test_suite='tests',
    description="Parse and create GEDCOM (genealogy) files",
    author="Rory McCann",
    author_email="rory@technomancy.org",
    classifiers=[
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Sociology :: Genealogy',
        'Topic :: Sociology :: History',
        'Topic :: Text Processing',
      ],
)
