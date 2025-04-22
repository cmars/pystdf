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

from pystdf.IO import Parser
from pystdf.Mapping import *
from pystdf.Writers import *

def main():
    filename, start, count = sys.argv[1:4]
    start = int(start)
    count = int(count)

    f = open(filename, 'rb')
    p=Parser(inp=f)
    record_mapper = StreamMapper()
    p.addSink(record_mapper)
    p.parse(count=start+count)
    p.addSink(AtdfWriter())
    f.seek(record_mapper.indexes[start])
    p.parse(count=count)

if __name__ == '__main__':
    main()

