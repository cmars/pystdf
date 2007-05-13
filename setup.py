#!/usr/bin/env python
#
# PySTDF - The Pythonic STDF Parser
# Copyright (C) 2006 Casey Marshall
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

import sys
from distutils.core import setup

setup(name='pystdf',
    version='1.3.2',
    description="Python module for working with STDF files",
    long_description="""
PySTDF is a Python module that makes it easy to work with STDF (Teradyne's Standard Test Data Format). STDF is a commonly used file format in semiconductor test -- automated test equipment (ATE) from such vendors as Teradyne, Verigy, LTX, Credence, and others support this format.

PySTDF provides event-based stream parsing of STDF version 4, along with indexers that can help you rearrange the data into a more useful tabular form, as well as generate missing summary records or new types of derivative records.

The parser architecture is very flexible and can easily be extended to support STDF version 3 as well as custom record types.

Potential applications of PySTDF include:
* Debugging a vendor's STDF implementation
* Straight conversion to ASCII-readable form
* Repairing STDF files
* Developing an application that leverages STDF
  - Conversion to tabular form for statistical analysis tools
  - Loading data into a relational database

PySTDF is released under a GPL license. Applications developed with PySTDF can only be released with a GPL-compatible license. Commercial applications can purchase an alternate license agreement for closed-source distribution.
""",
    author='Casey Marshall',
    author_email='casey.marshall@gmail.com',
    url='http://code.google.com/p/pystdf/',
    packages=['pystdf','pystdf.explorer'],
    scripts=['scripts/stdf_slice', 'scripts/rec_index', 'scripts/stdf2atdf'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'License :: Free for non-commercial use',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Intended Audience :: Manufacturing',
      'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
      'Topic :: Utilities',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Software Development :: Pre-processors',
      ],
)
