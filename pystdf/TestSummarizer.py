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
from pystdf.V4 import ptr, mpr, ftr, tsr

def filterNull(value):
  if value == 4294967295:
    return None
  return value
  
class TestSummarizer(EventSource):
  
  FLAG_SYNTH = 0x80
  FLAG_OVERALL = 0x01
  
  PTR_TEST_TXT = 0x00
  MPR_TEST_TXT = 0x01
  FTR_TEST_TXT = 0x02
  TSR_TEST_NAM = 0x03
  TSR_SEQ_NAME = 0x04
  TSR_TEST_LBL = 0x05
  
  def __init__(self):
    EventSource.__init__(self, ['testSummaryReady'])
  
  def testSummaryReady(self, dataSource): pass
  
  def getOverallTsrs(self):
    return self.overallTsrs.values()
  
  def getSiteTsrs(self):
    return self.summaryTsrs.values()
  
  def getSiteSynthTsrs(self):
    for siteTest, execCnt in self.testExecs.iteritems():
      site, test = siteTest
      tsrRow = [0, site, ' ', test,
        execCnt[0],
        self.testFails.get(siteTest, [0])[0],
        self.testInvalid.get(siteTest, [0])[0],
        None, None, None]
      yield tsrRow
  
  def before_begin(self, dataSource):
    self.testExecs = dict()
    self.testFails = dict()
    self.testInvalid = dict()
    self.summaryTsrs = dict()
    self.overallTsrs = dict()
    
    # Map of all test numbers to test names
    self.testAliasMap = dict()
    self.unitsMap = dict()
    self.limitsMap = dict()
    
    # Functional summary information
    self.cyclCntMap = dict()
    self.relVadrMap = dict()
    self.failPinMap = dict()
    
  def before_complete(self, dataSource):
    testKeys = set(self.testFails.keys())
    summaryTsrKeys = set(self.summaryTsrs.keys())
    
    # Determine which summary bin records need to be synthed
    # from part records.
    self.synthSummaryTsrKeys = testKeys - summaryTsrKeys
    
    # Determine which overall bin records need to be synthed
#    for siteTest, row in self.summaryTsrs.iteritems():
#      if not self.overallTsrs.has_key(siteTest[1]):
#        overallCount = self.synthOverallTsrs.setdefault(siteTest[1], [0])
#        overallCount[0] += row[tsr.FAIL_CNT]
#    for siteTest, partCount in self.testFails.iteritems():
#      if not self.overallTsrs.has_key(siteTest[1]):
#        overallCount = self.synthOverallTsrs.setdefault(siteTest[1], [0])
#        overallCount[0] += partCount[0]
    self.testSummaryReady(dataSource)
    
  def before_send(self, dataSource, data):
    table, row = data
    if table.name == ptr.name:
      self.onPtr(row)
    elif table.name == mpr.name:
      self.onMpr(row)
    elif table.name == ftr.name:
      self.onFtr(row)
    elif table.name == tsr.name:
      self.onTsr(row)
  
  def onPtr(self, row):
    execCount = self.testExecs.setdefault(
      (row[ptr.SITE_NUM], row[ptr.TEST_NUM]), [0])
    execCount[0] += 1
    if row[ptr.TEST_FLG] & 0x80 > 0:
      failCount = self.testFails.setdefault(
        (row[ptr.SITE_NUM], row[ptr.TEST_NUM]), [0])
      failCount[0] += 1
    if row[ptr.TEST_FLG] & 0x41 > 0:
      invalidCount = self.testInvalid.setdefault(
        (row[ptr.SITE_NUM], row[ptr.TEST_NUM]), [0])
      invalidCount[0] += 1
    aliases = self.testAliasMap.setdefault(row[ptr.TEST_NUM], set())
    aliases.add((row[ptr.TEST_TXT], self.PTR_TEST_TXT))
    if ptr.UNITS < len(row) and row[ptr.UNITS]:
      units = self.unitsMap.setdefault(row[ptr.TEST_NUM], [None])
      units[0] = row[ptr.UNITS]
    if row[ptr.OPT_FLAG] is not None and row[ptr.OPT_FLAG] & 0x40 == 0:
      loLimit = row[ptr.LO_LIMIT]
    else:
      loLimit = None
    if row[ptr.OPT_FLAG] is not None and row[ptr.OPT_FLAG] & 0x80 == 0:
      hiLimit = row[ptr.HI_LIMIT]
    else:
      hiLimit = None
    if loLimit is not None or hiLimit is not None:
      limits = self.limitsMap.setdefault(row[ptr.TEST_NUM], set())
      limits.add((loLimit, hiLimit))
  
  def onMpr(self, row):
    if row[mpr.TEST_FLG] & 0x80 > 0:
      failCount = self.testFails.setdefault(
        (row[mpr.SITE_NUM], row[mpr.TEST_NUM]), [0])
      failCount[0] += 1
    if row[ptr.TEST_FLG] & 0x41 > 0:
      invalidCount = self.testInvalid.setdefault(
        (row[ptr.SITE_NUM], row[ptr.TEST_NUM]), [0])
      invalidCount[0] += 1
    aliases = self.testAliasMap.setdefault(row[mpr.TEST_NUM], set())
    aliases.add((row[mpr.TEST_TXT], self.MPR_TEST_TXT))
    if mpr.UNITS < len(row) and row[mpr.UNITS]:
      units = self.unitsMap.setdefault(row[mpr.TEST_NUM], [None])
      units[0] = row[mpr.UNITS]
    if row[mpr.OPT_FLAG] is not None and row[mpr.OPT_FLAG] & 0x40 == 0:
      loLimit = row[mpr.LO_LIMIT]
    else:
      loLimit = None
    if row[mpr.OPT_FLAG] is not None and row[mpr.OPT_FLAG] & 0x80 == 0:
      hiLimit = row[mpr.HI_LIMIT]
    else:
      hiLimit = None
    if loLimit is not None or hiLimit is not None:
      limits = self.limitsMap.setdefault(row[mpr.TEST_NUM], set())
      limits.add((loLimit, hiLimit))
  
  def onFtr(self, row):
    if row[ftr.TEST_FLG] & 0x80 > 0:
      countList = self.testFails.setdefault(
        (row[ftr.SITE_NUM], row[ftr.TEST_NUM]), [0])
      countList[0] += 1
    
    if row[ftr.OPT_FLAG] is not None:
      if row[ftr.OPT_FLAG] & 0x01 > 0:
        countList = self.cyclCntMap.setdefault((row[ftr.TEST_NUM], row[ftr.CYCL_CNT]), [0])
        countList[0] += 1
      if row[ftr.OPT_FLAG] & 0x02 > 0:
        countList = self.relVadrMap.setdefault((row[ftr.TEST_NUM], row[ftr.REL_VADR]), [0])
        countList[0] += 1
      if ftr.RTN_STAT < len(row) and ftr.RTN_INDX < len(row) \
          and row[ftr.RTN_STAT] and row[ftr.RTN_INDX]:
        for i, rtnStat in enumerate(row[ftr.RTN_STAT]):
          if rtnStat > 4 and i < len(row[ftr.RTN_INDX]):   # A failing return state...
            pmrIndx = row[ftr.RTN_INDX][i]
            countList = self.failPinMap.setdefault((row[ftr.TEST_NUM], pmrIndx), [0])
            countList[0] += 1
    
    aliases = self.testAliasMap.setdefault(row[ftr.TEST_NUM], set())
    aliases.add((row[ftr.TEST_TXT], self.FTR_TEST_TXT))
  
  def onTsr(self, row):
    if row[tsr.HEAD_NUM] == 255:
      self.overallTsrs[row[tsr.TEST_NUM]] = [
        filterNull(value) for value in row]
    else:
      self.summaryTsrs[(row[tsr.SITE_NUM],row[tsr.TEST_NUM])] = [
        filterNull(value) for value in row]
    aliases = self.testAliasMap.setdefault(row[tsr.TEST_NUM], set())
    aliases.add((row[tsr.TEST_NAM], self.TSR_TEST_NAM))
    aliases.add((row[tsr.SEQ_NAME], self.TSR_SEQ_NAME))
    aliases.add((row[tsr.TEST_LBL], self.TSR_TEST_LBL))
  
