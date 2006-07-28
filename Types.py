import sys

from PySTDF import TableTemplate

logicalTypeMap = {
    "C1": "Char",
    "B1": "UInt8",
    "U1": "UInt8",
    "U2": "UInt16",
    "U4": "UInt32",
    "U8": "UInt64",
    "I1": "Int8",
    "I2": "Int16",
    "I4": "Int32",
    "I8": "Int64",
    "R4": "Float32",
    "R8": "Float64",
    "Cn": "String",
    "Bn": "List",
    "Dn": "List",
    "Vn": "List"
}

packFormatMap = {
    "C1": "c",
    "B1": "B",
    "U1": "B",
    "U2": "H",
    "U4": "I",
    "U8": "Q",
    "I1": "b",
    "I2": "h",
    "I4": "i",
    "I8": "q",
    "R4": "f",
    "R8": "d"
}

def stdfToLogicalType(fmt):
    if fmt.startswith('k'):
        return 'List'
    else:
        return logicalTypeMap[fmt]

class RecordHeader:
    def __init__(self):
        self.len=0
        self.typ=0
        self.sub=0

class RecordType(TableTemplate):
    def __init__(self):
        TableTemplate.__init__(self, 
            [name for name,stdfType in self.fieldMap], 
            [stdfToLogicalType(stdfTyp) for name,stdfTyp in self.fieldMap])
    
class EofException: pass

class EndOfRecordException: pass

class InitialSequenceException: pass
