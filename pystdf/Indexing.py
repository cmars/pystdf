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

from pystdf.OoHelpers import abstract
from pystdf import V4

class StreamIndexer:
  def before_header(self, dataSource, header):
    self.position = dataSource.inp.tell() - 4
    self.header = header

class SessionIndexer:
  def getSessionID(self):
    return self.sessionid

  def before_begin(self, dataSource):
    self.sessionid = self.createSessionID()

  def createSessionID(self): abstract()

class DemoSessionIndexer(SessionIndexer):
  def createSessionID(self): return 0

class RecordIndexer:
  def getRecID(self):
    return self.recid

  def before_begin(self, dataSource):
    self.recid = 0

  def before_send(self, dataSource, data):
    self.recid += 1

class MaterialIndexer:
  def getCurrentWafer(self, head):
    return self.currentWafer.get(head, 0)

  def getCurrentInsertion(self, head):
    return self.currentInsertion.get(head, 0)

  def getCurrentPart(self, head, site):
    return self.currentPart.get((head, site), 0)

  def before_begin(self, dataSource):
    self.currentPart = dict()
    self.currentInsertion = dict()
    self.closingInsertion = False
    self.currentWafer = dict()
    self.lastPart = 0
    self.lastInsertion = 0
    self.lastWafer = 0

  def before_send(self, dataSource, data):
    recType, fields = data

    if not isinstance(recType, V4.Prr) and self.closingInsertion:
      for head in self.currentInsertion.keys():
        self.currentInsertion[head] = 0
      self.closingInsertion = False

    if isinstance(recType, V4.Pir):
      headSite = (fields[V4.Pir.HEAD_NUM], fields[V4.Pir.SITE_NUM])
      self.onPir(headSite)
    elif isinstance(recType, V4.Wir):
      headSite = (fields[V4.Wir.HEAD_NUM], None) # fields[V4.Wir.SITE_NUM] Does not exist
      self.onWir(headSite)

  def after_send(self, dataSource, data):
    recType, fields = data
    if isinstance(recType, V4.Prr):
      headSite = (fields[V4.Prr.HEAD_NUM], fields[V4.Prr.SITE_NUM])
      self.onPrr(headSite)
    elif isinstance(recType, V4.Wrr):
      headSite = (fields[V4.Wrr.HEAD_NUM], None) # fields[V4.Wrr.SITE_NUM] Does not exist
      self.onWrr(headSite)

  def onPir(self, headSite):
    # Increment part count per site
    self.lastPart += 1
    self.currentPart[headSite] = self.lastPart

    # Increment insertion count once per head
    if self.currentInsertion.get(headSite[0], 0) == 0:
      self.lastInsertion += 1
      self.currentInsertion[headSite[0]] = self.lastInsertion

  def onPrr(self, headSite):
    self.currentPart[headSite] = 0
    self.closingInsertion = True

  def onWir(self, headSite):
    if self.currentWafer.get(headSite[0], 0) == 0:
      self.lastWafer += 1
      self.currentWafer[headSite[0]] = self.lastWafer

  def onWrr(self, headSite):
    self.currentWafer[headSite[0]]

