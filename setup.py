#!/usr/bin/env python

import sys
from distutils.core import setup
import py2exe

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.1.0"
        self.company_name = "Casey Marshall"
        self.copyright = "Copyright (c) Casey Marshall 2006, All Rights Reserved"
        self.name = "StdfExplorer"

################################################################
# A program using wxPython

# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store it in a file named
# test_wx.exe.manifest, and copy it with the data_files option into
# the dist-dir.
#
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

stdfexplorer_wx = Target(
    # used for the versioninfo resource
    description = "StdfExplorer version 1.1.0, Codename: Wax Tadpole",

    # what to build
    script = "pystdf/explorer/StdfExplorer.pyw",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="StdfExplorer"))],
##    icon_resources = [(1, "icon.ico")],
    dest_base = "StdfExplorer")

setup(name='pystdf',
    version='1.0.0',
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
#    windows=['pystdf/explorer/StdfExplorer.pyw',],
    windows = [stdfexplorer_wx],
    zipfile = None,
    options = {
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "ascii": 1,
            "bundle_files": 1,
            "packages": ['pystdf', 'pystdf.explorer'],
        }
    },
)
