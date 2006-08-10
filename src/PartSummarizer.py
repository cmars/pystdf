
from PySTDF import Pipeline
from PySTDF.SummaryStatistics import SummaryStatistics
from PySTDF.V4 import prr, pcr

def filterNull(value):
    if value == 4294967295:
        return None
    return value
    
class PartSummarizer(Pipeline.EventSource):
    
    FLAG_SYNTH = 0x80
    FLAG_FAIL = 0x08
    FLAG_UNKNOWN = 0x02
    FLAG_OVERALL = 0x01
    
    def __init__(self):
        EventSource.__init__(self, ['partSummaryReady'])
    
    def partSummaryReady(self, dataSource): pass
    
    def getOverall(self):
        return self.overall
    
    def getSiteCounts(self):
        return self.pcSummary.values()
    
    def getSiteSynthCounts(self):
        for site, info in self.pcSynth.iteritems():
            partCnt, goodCnt, abrtCnt = info
            yield [0, site, partCnt[0], None, 
                abrtCnt[0], goodCnt[0], None]
    
    def synthOverall(self):
        result = None
        for row in self.pcSummary.values():
            if result is None:
                result = [value for value in row]
            else:
                for i, value in enumerate(row):
                    if i > pcr.SITE_NUM and row[i] is not None:
                        if result[i] is None:
                            result[i] = row[i]
                        else:
                            result[i] += row[i]
        return result
    
    def before_begin(self, dataSource):
        self.pcSynth = dict()
        self.pcSummary = dict()
        self.overall = None
    
    def before_complete(self, dataSource):
        self.partSummaryReady(dataSource)
    
    def before_send(self, dataSource, data):
        table, row = data
        if table.name == prr.name:
            self.onPrr(row)
        elif table.name == pcr.name:
            self.onPcr(row)
    
    def onPrr(self, row):
        partCnt, goodCnt, abrtCnt = self.pcSynth.setdefault(row[prr.SITE_NUM], 
          ([0], [0], [0]))
        partCnt[0] += 1
        if row[prr.PART_FLG] & 0x08 == 0:
            goodCnt[0] += 1
        if row[prr.PART_FLG] & 0x04 == 0:
            abrtCnt[0] += 1
    
    def onPcr(self, row):
        if row[pcr.HEAD_NUM] == 255:
            self.overall = [
                filterNull(value) for value in row]
        else:
            self.pcSummary[row[pcr.SITE_NUM]] = [
                filterNull(value) for value in row]
    
