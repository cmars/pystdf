
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
        print index, rectype
    
