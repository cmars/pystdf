
import sys, os

class AtdfWriter:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
    def after_send(self, dataSource, data):
        self.stream.write('%s:%s%s' % (data[0].__class__.__name__,
            '|'.join([str(val) for val in data[1]]), os.linesep))
    def after_complete(self, dataSource):
        self.stream.flush()
