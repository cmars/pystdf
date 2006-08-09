
from PySTDF.IO import Parser
from PySTDF.Mapping import *
from PySTDF.Writers import *

if __name__ == '__main__':
    filename, start, count = sys.argv[1:4]
    start = int(start)
    count = int(count)
    
    f = open(filename, 'rb')
    p=Parser(inp=f)
    record_mapper = StreamMapper()
    p.addSink(record_mapper)
    p.parse(count=start+count)
    p.addSink(AtdfWriter())
    f.seek(record_mapper.indexes[start])
    p.parse(count=count)
