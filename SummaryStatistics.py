
class SummaryStatistics:
	def __init__(self, values):
		self.values = values
		self.min = min(values)
		self.max = max(values)
		self.count = len(values)
		self.sum = sum(values)
		self.sumsqrs = sum([value*value for value in values])
		self.mean = self.sum / float(self.count)
		self.median = self.q2 = self.values[self.count / 2]
		self.q1 = self.values[self.count / 4]
		self.q3 = self.values[3 * (self.count / 4)]
	
