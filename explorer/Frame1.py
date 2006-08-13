#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(2)]

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
              pos=wx.Point(327, 160), size=wx.Size(400, 494),
              style=wx.DEFAULT_FRAME_STYLE, title=u'STDF Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(392, 465))
        self.SetMenuBar(self.mainMenuBar)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnMenuHelpAboutMenu(self, event):
        event.Skip()
