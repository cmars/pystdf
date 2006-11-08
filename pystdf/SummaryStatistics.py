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
	
