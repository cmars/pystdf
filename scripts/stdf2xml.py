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

from __future__ import print_function
import sys, re

try:
    import gzip
    have_gzip = True
except ImportError:
    have_gzip = False
try:
    import bz2
    have_bz2 = True
except ImportError:
    have_bz2 = False

from pystdf.IO import Parser
from pystdf.Writers import XmlWriter
import pystdf.V4

gzPattern = re.compile(r'\.g?z', re.I)
bz2Pattern = re.compile(r'\.bz2', re.I)

def process_file(fnames):
    input_file = fnames[0]
    output_file = fnames[1] if len(fnames) > 1 else None

    reopen_fn = None
    if gzPattern.search(input_file):
        if not have_gzip:
            print("gzip not supported", file=sys.stderr)
            sys.exit(1)
        reopen_fn = lambda: gzip.open(input_file, 'rb')
        f = reopen_fn()
    elif bz2Pattern.search(input_file):
        if not have_bz2:
            print("bz2 not supported", file=sys.stderr)
            sys.exit(1)
        reopen_fn = lambda: bz2.BZ2File(input_file, 'rb')
        f = reopen_fn()
    else:
        f = open(input_file, 'rb')

    p = Parser(inp=f, reopen_fn=reopen_fn)

    # Handle output file
    if output_file:
        with open(output_file, 'w') as fout:
            p.addSink(XmlWriter(stream=fout))
            p.parse()
    else:
        p.addSink(XmlWriter())
        p.parse()

    f.close()

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <stdf file> [output xml file]")
    else:
        process_file(sys.argv[1:])

if __name__ == '__main__':
    main()

