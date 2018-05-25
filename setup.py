#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

setup(name="dynanets",
      version="0.1.0",
      description="Dynamic Processes over Dynamic Networks",
      license="GPL",
      author="André Panisson",
      author_email="panisson@gmail.com",
      url="http://github.com/panisson/dynanets",
      keywords= "mobility models",
      packages=["dynanets"],
      package_dir = {'': ''},
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'pandas'],
      classifiers=[
                   'License :: OSI-Approved Open Source :: GNU General Public License version 2.0 (GPLv2)',
                   'Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'Environment :: Console',
                   'User Interface :: Textual :: Command-line'
                   'Topic :: Scientific/Engineering :: Simulations',
                   'Topic :: Scientific/Engineering :: Network Analysis',
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: Science/Research',
                   ],
      )