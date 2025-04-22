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
# Modified: 2017 Minh-Hai Nguyen
#

import numpy as np
import pandas as pd
from pystdf.IO import Parser
from pystdf.Writers import TextWriter

class MemoryWriter:
    def __init__(self):
        self.data = []
    def after_send(self, dataSource, data):
        self.data.append(data)
    def write(self,line):
        self.data.append(line)
    def flush(self):
        pass # Do nothing

def ImportSTDF(fname):
    with open(fname,'rb') as fin:
        p = Parser(inp=fin)
        storage = MemoryWriter()
        p.addSink(storage)
        p.parse()
    return storage.data

def STDF2Text(fname,delimiter='|'):
    """ Convert STDF to a list of text representation
    """
    with open(fname,'rb') as fin:
        p = Parser(inp=fin)
        storage = MemoryWriter()
        p.addSink(TextWriter(storage,delimiter=delimiter))
        p.parse()
        return storage.data
    return None

def STDF2Dict(fname):
    """ Convert STDF to a list of dictionary objects
    """
    data = ImportSTDF(fname)
    data_out = []
    for datum in data:
        datum_out = {}
        RecType = datum[0].__class__.__name__.upper()
        datum_out['RecType'] = RecType
        for k,v in zip(datum[0].fieldMap,datum[1]):
            datum_out[k[0]] = v
        data_out.append(datum_out)
    return data_out

def STDF2DataFrame(fname):
    """ Convert STDF to a dictionary of DataFrame objects
    """
    data = ImportSTDF(fname)
    BigTable = {}
    for datum in data:
        RecType = datum[0].__class__.__name__.upper()
        if RecType not in BigTable.keys():
            BigTable[RecType] = {}
        Rec = BigTable[RecType]
        for k,v in zip(datum[0].fieldMap,datum[1]):
            if k[0] not in Rec.keys():
                Rec[k[0]] = []
            Rec[k[0]].append(v)
    for k,v in BigTable.items():
        BigTable[k] = pd.DataFrame(v)
    return BigTable
