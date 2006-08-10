
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
      headSite = (fields[V4.Pir.HEAD_NUM], fields[V4.Pir.SITE_NUM])
      self.onWir(headSite)
  
  def after_send(self, dataSource, data):
    recType, fields = data
    if isinstance(recType, V4.Prr):
      headSite = (fields[V4.Prr.HEAD_NUM], fields[V4.Prr.SITE_NUM])
      self.onPrr(headSite)
    elif isinstance(recType, V4.Prr):
      headSite = (fields[V4.Prr.HEAD_NUM], fields[V4.Prr.SITE_NUM])
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
  
  def onWrr(self, fields):
    self.currentWafer[headSite[0]]
  
