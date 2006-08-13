#Boa:Frame:Frame1

import wx
import wx.gizmos
from wx.lib.anchors import LayoutAnchors

from pystdf.IO import Parser
from pystdf.Mapping import *
from pystdf.Writers import *

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1STATUSBAR1, wxID_FRAME1TREELISTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(3)]

[wxID_FRAME1MENUFILECLOSE, wxID_FRAME1MENUFILEEXIT, wxID_FRAME1MENUFILEOPEN, 
] = [wx.NewId() for _init_coll_menuFile_Items in range(3)]

[wxID_FRAME1MENUHELPABOUT] = [wx.NewId() for _init_coll_menuHelp_Items in range(1)]

class Frame1(wx.Frame):
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

    def _init_coll_statusBar1_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text=u'Status')

        parent.SetStatusWidths([-1])

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
              pos=wx.Point(300, 141), size=wx.Size(615, 556),
              style=wx.DEFAULT_FRAME_STYLE, title=u'STDF Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(607, 527))
        self.SetMenuBar(self.mainMenuBar)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

        self.treeListCtrl1 = wx.gizmos.TreeListCtrl(id=wxID_FRAME1TREELISTCTRL1,
              name='treeListCtrl1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(607, 487), style=wx.TR_HAS_BUTTONS)
        self.treeListCtrl1.SetAutoLayout(False)
        self.treeListCtrl1.SetConstraints(LayoutAnchors(self.treeListCtrl1,
              True, True, False, False))

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
                
#                self.stdf_stream.seek(0)
#                self.parser = Parser(inp=self.stdf_stream)
#                self.parser.addSink(self.
#                self.parser
        
        finally:
            dlg.Destroy()
    
    def OnMenuFileCloseMenu(self, event):
        self.record_mapper = None
    
    def OnMenuFileExitMenu(self, event):
        self.Close()
    