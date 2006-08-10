
from pystdf.SummaryStatistics import SummaryStatistics
from pystdf.V4 import ptr, mpr
from pystdf.Pipeline import EventSource

class ParametricSummarizer(EventSource):
	
	def __init__(self):
		EventSource.__init__(self, ['parametricSummaryReady'])
	
	def parametricSummaryReady(self, dataSource): pass
	
	def getAllRows(self):
		return self.summaryMap.iteritems()
	
	def before_begin(self, dataSource):
		self.rawMap = dict()
		self.summaryMap = None
	
	def before_complete(self, dataSource):
		self.summaryMap = dict()
		for key, values in self.rawMap.iteritems():
			values.sort()
			self.summaryMap[key] = SummaryStatistics(values)
		self.parametricSummaryReady(dataSource)
	
	def before_send(self, dataSource, data):
		table, row = data
		if table.name == ptr.name:
			self.onPtr(row)
		elif table.name == mpr.name:
			self.onMpr(row)
	
	def onPtr(self, row):
		values = self.rawMap.setdefault((
			row[ptr.SITE_NUM],row[ptr.TEST_NUM],0), [])
		values.append(row[ptr.RESULT])
	
	def onMpr(self, row):
		for i in xrange(row[mpr.RSLT_CNT]):
			values = self.rawMap.setdefault((row[ptr.SITE_NUM],row[ptr.TEST_NUM],i), [])
			values.append(row[mpr.RTN_RSLT][i])
	
