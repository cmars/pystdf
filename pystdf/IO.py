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

import struct
import re

from pystdf.Types import *
from pystdf import V4

from pystdf.Pipeline import DataSource

def memorize(func):
  """Cache method results in instance's _field_parser_cache dict."""
  def wrapper(self, fieldType, count):
    cache = self.__dict__.setdefault('_field_parser_cache', {})
    return cache.setdefault((fieldType, count), func(self, fieldType, count))
  return wrapper

def groupConsecutiveDuplicates(fieldsList):
  """Groups consecutive identical field types and returns them with their counts.

  Examples:
    >>> groupConsecutiveDuplicates(['U4', 'U4', 'U1', 'C1', 'C1', 'C1'])
    [('U4', 2), ('U1', 1), ('C1', 3)]
    >>> groupConsecutiveDuplicates([])
    []
  """
  import itertools
  return (
      [(key, len(list(group))) for key, group in itertools.groupby(fieldsList)]
      if fieldsList
      else []
  )

class Parser(DataSource):
  _kFieldPattern = re.compile(r'k(\d+)([A-Z][a-z0-9]+)')

  def readAndUnpack(self, header, fmt):
    size = struct.calcsize(fmt)
    if (size > header.len):
      self.inp.read(header.len)
      header.len = 0
      raise EndOfRecordException()
    buf = self.inp.read(size)
    if len(buf) == 0:
      self.eof = 1
      raise EofException()
    if len(buf) < size:
      header.len = 0
      raise EndOfRecordException()
    header.len -= len(buf)
    val,=struct.unpack(self.endian + fmt, buf)
    if isinstance(val,bytes):
        return val.decode("ascii")
    else:
        return val

  def readAndUnpackDirect(self, fmt):
    size = struct.calcsize(fmt)
    buf = self.inp.read(size)
    if len(buf) == 0:
      self.eof = 1
      raise EofException()
    val,=struct.unpack(self.endian + fmt, buf)
    return val

  def readField(self, header, stdfFmt):
    return self.readAndUnpack(header, packFormatMap[stdfFmt])

  def readFieldDirect(self, stdfFmt):
    return self.readAndUnpackDirect(packFormatMap[stdfFmt])

  def batchReadFields(self, header, stdfFmt, count):
    fmt = packFormatMap[stdfFmt]
    size = struct.calcsize(fmt)
    totalSize = size * count
    if (totalSize > header.len):
      fullCount = header.len // size
      if not fullCount:
        header.len = 0
        return (None,) * count
      tmpResult = list(self.batchReadFields(header, stdfFmt, fullCount))
      header.len = 0
      tmpResult.extend([None] * (count - fullCount))
      return tuple(tmpResult)
    buf = self.inp.read(totalSize)
    if len(buf) == 0:
      self.eof = 1
      raise EofException()
    header.len -= totalSize
    vals = struct.unpack(self.endian + fmt * count, buf)
    if isinstance(vals[0],bytes):
      return tuple(val.decode("ascii") for val in vals)
    else:
      return vals

  def readCn(self, header):
    if header.len == 0:
      raise EndOfRecordException()
    slen = self.readField(header, "U1")
    if slen > header.len:
      self.inp.read(header.len)
      header.len = 0
      raise EndOfRecordException()
    if slen == 0:
      return ""
    buf = self.inp.read(slen);
    if len(buf) == 0:
      self.eof = 1
      raise EofException()
    header.len -= len(buf)
    val,=struct.unpack(str(slen) + "s", buf)
    return val.decode("ascii")

  def readBn(self, header):
    blen = self.readField(header, "U1")
    bn = []
    for i in range(0, blen):
      bn.append(self.readField(header, "B1"))
    return bn

  def readDn(self, header):
    dbitlen = self.readField(header, "U2")
    dlen = dbitlen / 8
    if dbitlen % 8 > 0:
      dlen+=1
    dn = []
    for i in range(0, int(dlen)):
      dn.append(self.readField(header, "B1"))
    return dn

  def readVn(self, header):
    vlen = self.readField(header, "U2")
    vn = []
    for i in range(0, vlen):
      fldtype = self.readField(header, "B1")
      if fldtype in self.vnMap:
        vn.append(self.vnMap[fldtype](header))
    return vn

  def readArray(self, header, indexValue, stdfFmt):
    if (stdfFmt == 'N1'):
      return self.readArray(header, indexValue/2+indexValue%2, 'U1')
    arr = []
    for i in range(int(indexValue)):
      arr.append(self.unpackMap[stdfFmt](header, stdfFmt))
    return arr

  def readHeader(self):
    hdr = RecordHeader()
    hdr.len = self.readFieldDirect("U2")
    hdr.typ = self.readFieldDirect("U1")
    hdr.sub = self.readFieldDirect("U1")
    return hdr

  def __detectEndian(self):
    self.eof = 0
    header = self.readHeader()
    if header.typ != 0 and header.sub != 10:
      raise InitialSequenceException()
    cpuType = self.readFieldDirect("U1")
    if self.reopen_fn:
      self.inp = self.reopen_fn()
    else:
      self.inp.seek(0)
    if cpuType == 2:
      return '<'
    else:
      return '>'

  def header(self, header): pass

  def parse_records(self, count=0):
    i = 0
    self.eof = 0
    fields = None
    try:
      while self.eof==0:
        header = self.readHeader()
        self.header(header)
        if (header.typ, header.sub) in self.recordMap:
          recType = self.recordMap[(header.typ, header.sub)]
          recParser = self.recordParsers[(header.typ, header.sub)]
          fields = recParser(self, header, [])
          if len(fields) < len(recType.columnNames):
            fields += [None] * (len(recType.columnNames) - len(fields))
          self.send((recType, fields))
          if header.len > 0:
            print(
              "Warning: Broken header. Unprocessed data left in record of type '%s'. Working around it." % recType.__class__.__name__,
              file=sys.stderr,
            )
            self.inp.read(header.len)
            header.len = 0
        else:
          self.inp.read(header.len)
        if count:
          i += 1
          if i >= count: break
    except EofException: pass

  def auto_detect_endian(self):
    if self.inp.tell() == 0:
      self.endian = '@'
      self.endian = self.__detectEndian()

  def parse(self, count=0):
    self.begin()

    try:
      self.auto_detect_endian()
      self.parse_records(count)
      self.complete()
    except Exception as exception:
      self.cancel(exception)
      raise

  @memorize
  def getFieldParser(self, fieldType, count):
    if (fieldType.startswith("k")):
      fieldIndex, arrayFmt = self._kFieldPattern.match(fieldType).groups()
      def parseDynamicArray(parser, header, fields):
        return parser.readArray(header, fields[int(fieldIndex)], arrayFmt)
      return parseDynamicArray, count
    if fieldType in self._unpackMap:
      def parseBatchedFields(parser, header, fields):
        result = parser.batchReadFields(header, fieldType, count)
        return result
      return parseBatchedFields, 1
    parseFn = self.unpackMap[fieldType]
    def parseIndividualFields(parser, header, fields):
      return parseFn(header, fieldType)
    return parseIndividualFields, count

  def createRecordParser(self, recType):
    fieldParsers = []
    groupedFields = groupConsecutiveDuplicates(recType.fieldStdfTypes)
    for (stdfType, count) in groupedFields:
      func, times = self.getFieldParser(stdfType, count)
      for _ in range(times):
        fieldParsers.append(func)

    def fn(parser, header, fields):
      try:
        for parseField in fieldParsers:
          result = parseField(parser, header, fields)
          if isinstance(result, tuple):
            fields.extend(result)
          else:
            fields.append(result)
      except EndOfRecordException: pass
      return fields
    return fn

  def __init__(self, recTypes=V4.records, inp=sys.stdin, reopen_fn=None, endian=None):
    DataSource.__init__(self, ['header']);
    self.eof = 1
    self.recTypes = set(recTypes)
    self.inp = inp
    self.reopen_fn = reopen_fn
    self.endian = endian

    self.recordMap = dict(
      [ ( (recType.typ, recType.sub), recType )
        for recType in recTypes ])

    self._unpackMap = {
      ftype: self.readField 
      for ftype in ("C1", "B1", "U1", "U2", "U4", "U8", 
                  "I1", "I2", "I4", "I8", "R4", "R8")
    }
    self.unpackMap = {
      **self._unpackMap,
      **{
        "Cn": lambda header, _: self.readCn(header),
        "Bn": lambda header, _: self.readBn(header),
        "Dn": lambda header, _: self.readDn(header),
        "Vn": lambda header, _: self.readVn(header)
      }
    }

    self.recordParsers = dict(
      [ ( (recType.typ, recType.sub), self.createRecordParser(recType) )
        for recType in recTypes ])

    self.vnMap = {
      0: lambda header: self.inp.read(header, 1),
      1: lambda header: self.readField(header, "U1"),
      2: lambda header: self.readField(header, "U2"),
      3: lambda header: self.readField(header, "U4"),
      4: lambda header: self.readField(header, "I1"),
      5: lambda header: self.readField(header, "I2"),
      6: lambda header: self.readField(header, "I4"),
      7: lambda header: self.readField(header, "R4"),
      8: lambda header: self.readField(header, "R8"),
      10: lambda header: self.readCn(header),
      11: lambda header: self.readBn(header),
      12: lambda header: self.readDn(header),
      13: lambda header: self.readField(header, "U1")
    }
