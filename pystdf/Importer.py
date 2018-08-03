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
import re

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

gzPattern = re.compile('\.g?z', re.I)
bz2Pattern = re.compile('\.bz2', re.I)

class MemoryWriter:
    def __init__(self):
        self.data = []
    def after_send(self, dataSource, data):
        self.data.append(data)
    def write(self,line):
        self.data.append(line)
    def flush(self):
        pass # Do nothing

def OpenSTDFparser(fname):
    reopen_fn = None
    if gzPattern.search(fname):
        if not have_gzip:
            raise RuntimeError('gzip is not supported on this system')
        reopen_fn = lambda: gzip.open(fname, 'rb')
        f = reopen_fn()
    elif bz2Pattern.search(fname):
        if not have_bz2:
            raise RuntimeError('bz2 is not supported on this system')
        reopen_fn = lambda: bz2.BZ2File(fname, 'rb')
        f = reopen_fn()
    else:
        f = open(fname, 'rb')
    p = Parser(inp=f, reopen_fn=reopen_fn)
    return p, f

def ImportSTDF(fname):
    p, f = OpenSTDFparser(fname)
    storage = MemoryWriter()
    p.addSink(storage)
    p.parse()
    f.close()
    return storage.data

def STDF2Text(fname,delimiter='|'):
    """ Convert STDF to a list of text representation
    """
    p, f = OpenSTDFparser(fname)
    storage = MemoryWriter()
    p.addSink(TextWriter(storage,delimiter=delimiter))
    p.parse()
    f.close()
    return storage.data

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
