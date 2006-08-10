
import sys, os
from time import strftime, localtime
from pystdf import V4

class AtdfWriter:
    
    @staticmethod
    def atdf_format(rectype, field_index, value):
        field_type = rectype.fieldStdfTypes[field_index]
        if value is None:
            return ""
        elif rectype is V4.gdr:
            return '|'.join([str(v) for v in value])
        elif field_type[0] == 'k':
            return ','.join([format_by_type(v, field_type[2:]) for v in value])
        elif rectype is V4.mir or rectype is V4.mrr:
            field_name = rectype.fieldNames[field_index]
            if field_name.endswith('_T'):
                return strftime('%H:%M:%S %d-%b-%Y', localtime(value))
            else:
                return str(value)
        else:
            return str(value)
    
    def __init__(self, stream=sys.stdout):
        self.stream = stream
    
    def after_send(self, dataSource, data):
        line = '%s:%s%s' % (data[0].__class__.__name__,
            '|'.join([self.atdf_format(data[0], i, val) for i, val in enumerate(data[1])]), '\n')
        self.stream.write(line)
    
    def after_complete(self, dataSource):
        self.stream.flush()
