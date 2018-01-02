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

import sys, os
from time import strftime, localtime
from xml.sax.saxutils import quoteattr
from pystdf import V4

import pdb

def format_by_type(value, field_type):
    if field_type in ('B1', 'N1'):
        return '%02X' % (value)
    else:
        return str(value)

class TextWriter:
    def __init__(self, stream=sys.stdout, delimiter='|'):
        self.stream = stream
        self.delimiter = delimiter

    @staticmethod
    def text_format(rectype, field_index, value):
        field_type = rectype.fieldStdfTypes[field_index]
        if value is None:
            return ""
        elif rectype is V4.gdr:
            return self.delimiter.join([str(v) for v in value])
        elif field_type[0] == 'k': # An Array of some other type
            return ','.join([format_by_type(v, field_type[2:]) for v in value])
        elif rectype is V4.mir or rectype is V4.mrr:
            field_name = rectype.fieldNames[field_index]
            if field_name.endswith('_T'): # A Date-Time in an MIR/MRR
                return strftime('%H:%M:%S %d-%b-%Y', localtime(value))
            else:
                return str(value)
        else:
            return str(value)

    def after_send(self, dataSource, data):
        line = '%s%s%s\n' % (data[0].__class__.__name__.upper(),self.delimiter,
            self.delimiter.join([self.text_format(data[0], i, val) for i, val in enumerate(data[1])]))
        self.stream.write(line)

    def after_complete(self, dataSource):
        self.stream.flush()

class XmlWriter:
    extra_entities = {'\0': ''}

    @staticmethod
    def xml_format(rectype, field_index, value):
        field_type = rectype.fieldStdfTypes[field_index]
        if value is None:
            return ""
        elif rectype is V4.gdr:
            return ';'.join([str(v) for v in value])
        elif field_type[0] == 'k': # An Array of some other type
            return ','.join([format_by_type(v, field_type[2:]) for v in value])
        elif rectype is V4.mir or rectype is V4.mrr:
            field_name = rectype.fieldNames[field_index]
            if field_name.endswith('_T'): # A Date-Time in an MIR/MRR
                return strftime('%H:%M:%ST%d-%b-%Y', localtime(value))
            else:
                return str(value)
        else:
            return str(value)

    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def before_begin(self, dataSource):
        self.stream.write('<Stdf>\n')

    def after_send(self, dataSource, data):
        self.stream.write('<%s' % (data[0].__class__.__name__))
        for i, val in enumerate(data[1]):
            fmtval = self.xml_format(data[0], i, val)
            self.stream.write(' %s=%s' % (data[0].fieldNames[i], quoteattr(fmtval, self.extra_entities)))
        self.stream.write('/>\n')

    def after_complete(self, dataSource):
        self.stream.write('</Stdf>\n')
        self.stream.flush()
