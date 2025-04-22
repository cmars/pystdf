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

from pystdf.Types import *
from pystdf.Indexing import *
from pystdf import V4

class StreamMapper(StreamIndexer):

    def __init__(self, types=V4.records):
        self.indexes = []
        self.types = []
        self.__rec_map = dict([((recType.typ, recType.sub), recType)
                                for recType in types])

    def before_header(self, dataSource, header):
        StreamIndexer.before_header(self, dataSource, header)
        self.indexes.append(self.position)
        key = (self.header.typ, self.header.sub)
        rectype = self.__rec_map.get(key, UnknownRecord(*key))
        self.types.append(rectype)

class MaterialMapper(MaterialIndexer):
    indexable_types = set([V4.wir, V4.wrr, V4.pir, V4.prr, V4.ptr, V4.mpr, V4.ftr])
    per_part_types = set([V4.pir, V4.prr, V4.ptr, V4.mpr, V4.ftr])

    def before_begin(self, dataSource):
        MaterialIndexer.before_begin(self, dataSource)
        self.waferid = []
        self.insertionid = []
        self.partid = []

    def before_send(self, dataSource, data):
        MaterialIndexer.before_send(self, dataSource, data)
        rectype, rec = data
        if rectype in self.indexable_types:
            head = rec[rectype.HEAD_NUM]
            self.waferid.append(self.getCurrentWafer(head))
            self.insertionid.append(self.getCurrentInsertion(head))
            if rectype in self.per_part_types:
                site = rec[rectype.SITE_NUM]
                self.partid.append(self.getCurrentPart(head, site))
            else:
                self.partid.append(None)
        else:
            self.waferid.append(None)
            self.insertionid.append(None)
            self.partid.append(None)

if __name__ == '__main__':
    from pystdf.IO import Parser
    from pystdf.Writers import AtdfWriter
    import pystdf.V4

    filename, = sys.argv[1:]
    f = open(filename, 'rb')
    p=Parser(inp=f)
    record_mapper = StreamMapper()
    p.addSink(record_mapper)
    p.parse()
    f.close()

    for index, rectype in zip(record_mapper.indexes, record_mapper.types):
        print(index, rectype)
