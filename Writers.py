
import sys, os

class AtdfWriter:
    @staticmethod
    def atdf_format(rectype, field_index, value):
        if value is None:
            return ''
        else:
            return str(value) # TODO: Correct formatting for all types!
    
    def __init__(self, stream=sys.stdout):
        self.stream = stream
    def after_send(self, dataSource, data):
        self.stream.write('%s:%s%s' % (data[0].__class__.__name__,
            '|'.join([self.atdf_format(data[0], i, val) for i, val in enumerate(data[1])]), os.linesep))
    def after_complete(self, dataSource):
        self.stream.flush()
