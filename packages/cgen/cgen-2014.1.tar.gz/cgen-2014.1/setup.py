#!/usr/bin/env python
# -*- coding: latin1 -*-

from setuptools import setup

setup(
        name="cgen",
        version="2014.1",
        description="C/C++ source generation from an AST",
        long_description="""
            See `documentation <http://documen.tician.de/cgen/>`_
            and `git tree <http://github.com/inducer/cgen>`_.
            """,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: Other Audience',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development :: Libraries',
            'Topic :: Utilities',
            ],

        author="Andreas Kloeckner",
        author_email="inform@tiker.net",
        license="MIT",
        url="http://documen.tician.de/cgen/",

        packages=["cgen"],
        install_requires=[
            "pytools>=8",
            ])
