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

from pystdf.Pipeline import EventSource
from pystdf.SummaryStatistics import SummaryStatistics
from pystdf.V4 import prr, hbr, sbr

def ifElse(cond, trueVal, falseVal):
  if cond:
    return trueVal
  else:
    return falseVal

class BinSummarizer(EventSource):
  
  FLAG_SYNTH = 0x80
  FLAG_FAIL = 0x08
  FLAG_UNKNOWN = 0x02
  FLAG_OVERALL = 0x01
  
  def __init__(self):
    EventSource.__init__(self, ['binSummaryReady'])
  
  def binSummaryReady(self, dataSource): pass
  
  def getHPfFlags(self, row):
    flag = 0
    if row[hbr.HBIN_PF] == 'F':
      flag |= self.FLAG_FAIL
    elif row[hbr.HBIN_PF] != 'P':
      flag |= self.FLAG_UNKNOWN
    return flag
  
  def getSPfFlags(self, row):
    flag = 0
    if row[sbr.SBIN_PF] == 'F':
      flag |= self.FLAG_FAIL
    elif row[sbr.SBIN_PF] != 'P':
      flag |= self.FLAG_UNKNOWN
    return flag
  
  def getOverallHbins(self):
    return self.overallHbrs.values()
  
  def getSiteHbins(self):
    return self.summaryHbrs.values()
  
  def getSiteSynthHbins(self):
    for siteBin, info in self.hbinParts.iteritems():
      site, bin = siteBin
      partCount, isPass = info
      if isPass[0]:
        pf = 'P'
      else:
        pf = 'F'
      row = [0, site, bin, partCount[0], pf, None]
      yield row
  
  def getOverallSbins(self):
    return self.overallSbrs.values()
  
  def getSiteSbins(self):
    return self.summarySbrs.values()
  
  def getSiteSynthSbins(self):
    for siteBin, info in self.sbinParts.iteritems():
      site, bin = siteBin
      partCount, isPass = info
      if isPass[0]:
        pf = 'P'
      else:
        pf = 'F'
      row = [0, site, bin, partCount[0], pf, None]
      yield row
  
  def before_begin(self, dataSource):
    self.hbinParts = dict()
    self.sbinParts = dict()
    self.summaryHbrs = dict()
    self.summarySbrs = dict()
    self.overallHbrs = dict()
    self.overallSbrs = dict()
    
  def before_complete(self, dataSource):
    self.binSummaryReady(dataSource)
  
  def before_send(self, dataSource, data):
    table, row = data
    if table.name == prr.name:
      self.onPrr(row)
    elif table.name == hbr.name:
      self.onHbr(row)
    elif table.name == sbr.name:
      self.onSbr(row)
  
  def ifElse(cond, trueVal, falseVal):
    if cond:
      return trueVal
    else:
      return falseVal
  
  def onPrr(self, row):
    countList, passList = self.hbinParts.setdefault(
      (row[prr.SITE_NUM], row[prr.HARD_BIN]), ([0], [None]))
    countList[0] += 1
    if passList[0] is None:
      passList[0] = ifElse(row[prr.PART_FLG] & 0x08 == 0, 'P', 'F')
    elif passList[0] != ' ':
      if passList[0] != ifElse(row[prr.PART_FLG] & 0x08 == 0, 'P', 'F'):
        passList[0] = ' '
    
    countList, passList = self.sbinParts.setdefault(
      (row[prr.SITE_NUM], row[prr.SOFT_BIN]), ([0], [False]))
    countList[0] += 1
    if passList[0] is None:
      passList[0] = ifElse(row[prr.PART_FLG] & 0x08 == 0, 'P', 'F')
    elif passList[0] != ' ':
      if passList[0] != ifElse(row[prr.PART_FLG] & 0x08 == 0, 'P', 'F'):
        passList[0] = ' '
  
  def onHbr(self, row):
    if row[hbr.HEAD_NUM] == 255:
      self.overallHbrs[row[hbr.HBIN_NUM]] = row
    else:
      self.summaryHbrs[(row[hbr.SITE_NUM], row[hbr.HBIN_NUM])] = row
    
  def onSbr(self, row):
    if row[sbr.HEAD_NUM] == 255:
      self.overallSbrs[row[sbr.SBIN_NUM]] = row
    else:
      self.summarySbrs[(row[sbr.SITE_NUM], row[sbr.SBIN_NUM])] = row
  
