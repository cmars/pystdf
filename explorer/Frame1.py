#Boa:Frame:Frame1

import wx
import wx.grid
import wx.gizmos
from wx.lib.anchors import LayoutAnchors

from pystdf.IO import Parser
from pystdf.Mapping import *
from pystdf.Writers import *

from record_pos_table import RecordPositionTable
from record_pos_listctrl import RecordPositionListCtrl
from record_view_listctrl import RecordViewListCtrl
from record_keeper import RecordKeeper

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1RECORDPOSITIONLIST, wxID_FRAME1RECORDVIEWLIST, 
 wxID_FRAME1STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(4)]

[wxID_FRAME1MENUFILECLOSE, wxID_FRAME1MENUFILEEXIT, wxID_FRAME1MENUFILEOPEN, 
] = [wx.NewId() for _init_coll_menuFile_Items in range(3)]

[wxID_FRAME1MENUHELPABOUT] = [wx.NewId() for _init_coll_menuHelp_Items in range(1)]

class Frame1(wx.Frame):
    _custom_classes = {'wx.ListCtrl': ['RecordPositionListCtrl','RecordViewListCtrl']}
    
    def _init_coll_mainSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.recordPositionList, 1, border=0, flag=0)
        parent.AddWindow(self.recordViewList, 2, border=0, flag=0)

    def _init_coll_mainMenuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title=u'File')
        parent.Append(menu=self.menuHelp, title=u'Help')

    def _init_coll_menuHelp_Items(self, parent):
        # generated method, don't edit

        parent.Append(help=u'', id=wxID_FRAME1MENUHELPABOUT,
              kind=wx.ITEM_NORMAL, text=u'About')
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
              id=wxID_FRAME1MENUHELPABOUT)

    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1MENUFILEOPEN, kind=wx.ITEM_NORMAL,
              text=u'Open')
        parent.Append(help='', id=wxID_FRAME1MENUFILECLOSE, kind=wx.ITEM_NORMAL,
              text=u'Close')
        parent.Append(help='', id=wxID_FRAME1MENUFILEEXIT, kind=wx.ITEM_NORMAL,
              text=u'Exit')
        self.Bind(wx.EVT_MENU, self.OnMenuFileOpenMenu,
              id=wxID_FRAME1MENUFILEOPEN)
        self.Bind(wx.EVT_MENU, self.OnMenuFileCloseMenu,
              id=wxID_FRAME1MENUFILECLOSE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExitMenu,
              id=wxID_FRAME1MENUFILEEXIT)

    def _init_coll_recordViewList_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'Field Name', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, heading=u'Value',
              width=-1)

    def _init_coll_recordPositionList_Columns(self, parent):
        # generated method, don't edit

        parent.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT,
              heading=u'File Offset', width=-1)
        parent.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT,
              heading=u'Record Type', width=-1)

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text=u'Status')

        parent.SetStatusWidths([-1])

    def _init_sizers(self):
        # generated method, don't edit
        self.mainSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_mainSizer_Items(self.mainSizer)

        self.SetSizer(self.mainSizer)

    def _init_utils(self):
        # generated method, don't edit
        self.menuFile = wx.Menu(title='')

        self.menuHelp = wx.Menu(title='')

        self.mainMenuBar = wx.MenuBar()

        self._init_coll_menuFile_Items(self.menuFile)
        self._init_coll_menuHelp_Items(self.menuHelp)
        self._init_coll_mainMenuBar_Menus(self.mainMenuBar)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(304, 125), size=wx.Size(615, 556),
              style=wx.DEFAULT_FRAME_STYLE, title=u'STDF Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(607, 527))
        self.SetMenuBar(self.mainMenuBar)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.recordPositionList = RecordPositionListCtrl(id=wxID_FRAME1RECORDPOSITIONLIST,
              name=u'recordPositionList', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(202, 487),
              style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self._init_coll_recordPositionList_Columns(self.recordPositionList)
        self.recordPositionList.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnRecordPositionListListItemSelected,
              id=wxID_FRAME1RECORDPOSITIONLIST)

        self.recordViewList = RecordViewListCtrl(id=wxID_FRAME1RECORDVIEWLIST,
              name=u'recordViewList', parent=self, pos=wx.Point(202, 0),
              size=wx.Size(404, 487),
              style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self.recordViewList.SetAutoLayout(False)
        self.recordViewList.SetMinSize(wx.Size(404, 487))
        self._init_coll_recordViewList_Columns(self.recordViewList)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.stdf_stream = None
    
    def OnMenuHelpAboutMenu(self, event):
        event.Skip()
    
    def OnMenuFileOpenMenu(self, event):
        dlg = wx.FileDialog(self, "Choose a file", ".", "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                self.stdf_stream = open(filename, 'rb')
                
                parser = Parser(inp=self.stdf_stream)
                self.record_mapper = StreamMapper()
                parser.addSink(self.record_mapper)
                parser.parse()
                
                self.recordPositionList.record_mapper = self.record_mapper
                
                self.stdf_stream.seek(0)
                self.parser = Parser(inp=self.stdf_stream)
                self.record_keeper = RecordKeeper()
                self.parser.addSink(self.record_keeper)
                self.parser.parse(1)
            
        finally:
            dlg.Destroy()
    
    def OnMenuFileCloseMenu(self, event):
        self.recordPositionList.record_mapper = None
        del self.stdf_stream
        self.stdf_stream = None
        self.parser = None
        self.record_mapper = None
    
    def OnMenuFileExitMenu(self, event):
        self.Close()
    
    def OnRecordPositionListListItemSelected(self, event):
        if self.record_mapper:
            self.stdf_stream.seek(self.record_mapper.indexes[event.GetIndex()])
            self.parser.parse(1)
            print self.record_keeper.record_type, self.record_keeper.record_data
            self.recordViewList.record = self.record_keeper.record_type, self.record_keeper.record_data 
    
