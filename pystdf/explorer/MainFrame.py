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

#Boa:Frame:MainFrame

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

from threading import *
from pystdf.logexcept import exc_string

# Define notification event for thread completion
EVT_MAPPED_ID = wx.Window.NewControlId()

def EVT_MAPPED(win, func):
    """Define Mapped Event."""
    win.Connect(-1, -1, EVT_MAPPED_ID, func)

class MappedEvent(wx.PyEvent):
    def __init__(self, cancelled=False):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_MAPPED_ID)
        self.cancelled = cancelled

class ProgressUpdater:
    def __init__(self, notify_window):
        self.notify_window = notify_window
        self.count = 0
        self.cancelled = False

    def before_send(self, dataSource, data):
        if self.cancelled:
            raise MapperCancelled
        self.count += 1
        if self.count % 1000 == 0:
            self.notify_window.statusBar.SetStatusText('Mapped %d bytes' % (
                dataSource.inp.tell()))
            self.notify_window.recordPositionList.SetItemCount(self.count)

class MapperCancelled(Exception): pass

class MapperThread(Thread):
    def __init__(self, notify_window, parser):
        Thread.__init__(self)
        self._notify_window = notify_window
        self.parser = parser
        self.progress_updater = ProgressUpdater(notify_window)
        self.parser.addSink(self.progress_updater)
        self.start()

    def cancel(self):
        self.progress_updater.cancelled = True

    def run(self):
        try:
            self.parser.parse()
            wx.PostEvent(self._notify_window, MappedEvent())
        # except Exception, what:
        except Exception as what:
            print >>sys.stderr, exc_string()
            wx.PostEvent(self._notify_window, MappedEvent(cancelled=True))

def create(parent):
    return MainFrame(parent)

[wxID_MAINFRAME, wxID_MAINFRAMERECORDPOSITIONLIST,
 wxID_MAINFRAMERECORDVIEWLIST, wxID_MAINFRAMESTATUSBAR,
] = [wx.Window.NewControlId() for _init_ctrls in range(4)]

[wxID_MAINFRAMEMENUFILECLOSE, wxID_MAINFRAMEMENUFILEEXIT,
 wxID_MAINFRAMEMENUFILEOPEN,
] = [wx.Window.NewControlId() for _init_coll_menuFile_Items in range(3)]

[wxID_MAINFRAMEMENUHELPABOUT] = [wx.Window.NewControlId() for _init_coll_menuHelp_Items in range(1)]

class MainFrame(wx.Frame):
    _custom_classes = {'wx.ListCtrl': ['RecordPositionListCtrl','RecordViewListCtrl']}

    def _init_coll_mainSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.recordPositionList, 1, border=0, flag=0)
        parent.Add(self.recordViewList, 2, border=0, flag=0)

    def _init_coll_mainMenuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menuFile, title=u'File')
        parent.Append(menu=self.menuHelp, title=u'Help')

    def _init_coll_menuHelp_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_MAINFRAMEMENUHELPABOUT,
              kind=wx.ITEM_NORMAL, item=u'About')
        self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
              id=wxID_MAINFRAMEMENUHELPABOUT)

    def _init_coll_menuFile_Items(self, parent):
        # generated method, don't edit

        parent.Append(id=wxID_MAINFRAMEMENUFILEOPEN,
              kind=wx.ITEM_NORMAL, item=u'Open')
        parent.Append(id=wxID_MAINFRAMEMENUFILECLOSE,
              kind=wx.ITEM_NORMAL, item=u'Close')
        parent.Append(id=wxID_MAINFRAMEMENUFILEEXIT,
              kind=wx.ITEM_NORMAL, item=u'Exit')
        self.Bind(wx.EVT_MENU, self.OnMenuFileOpenMenu,
              id=wxID_MAINFRAMEMENUFILEOPEN)
        self.Bind(wx.EVT_MENU, self.OnMenuFileCloseMenu,
              id=wxID_MAINFRAMEMENUFILECLOSE)
        self.Bind(wx.EVT_MENU, self.OnMenuFileExitMenu,
              id=wxID_MAINFRAMEMENUFILEEXIT)

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
        parent.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT,
              heading=u'Wafer', width=-1)
        parent.InsertColumn(col=3, format=wx.LIST_FORMAT_LEFT,
              heading=u'Insertion', width=-1)
        parent.InsertColumn(col=4, format=wx.LIST_FORMAT_LEFT,
              heading=u'Part', width=-1)

    def _init_coll_statusBar_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(u'Status')

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
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name=u'MainFrame',
              parent=prnt, pos=wx.Point(304, 125), size=wx.Size(615, 556),
              style=wx.DEFAULT_FRAME_STYLE, title=u'STDF Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(607, 527))
        self.SetMenuBar(self.mainMenuBar)
        self.SetExtraStyle(0)
        self.SetStatusBarPane(0)

        self.statusBar = wx.StatusBar(id=wxID_MAINFRAMESTATUSBAR,
              name=u'statusBar', parent=self, style=0)
        self._init_coll_statusBar_Fields(self.statusBar)
        self.SetStatusBar(self.statusBar)

        self.recordPositionList = RecordPositionListCtrl(id=wxID_MAINFRAMERECORDPOSITIONLIST,
              name=u'recordPositionList', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(202, 487),
              style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self._init_coll_recordPositionList_Columns(self.recordPositionList)
        self.recordPositionList.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnRecordPositionListListItemSelected,
              id=wxID_MAINFRAMERECORDPOSITIONLIST)

        self.recordViewList = RecordViewListCtrl(id=wxID_MAINFRAMERECORDVIEWLIST,
              name=u'recordViewList', parent=self, pos=wx.Point(202, 0),
              size=wx.Size(404, 487),
              style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_HRULES | wx.LC_VRULES)
        self.recordViewList.SetAutoLayout(False)
        self.recordViewList.SetMinSize(wx.Size(404, 487))
        self._init_coll_recordViewList_Columns(self.recordViewList)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.view_stream = None
        EVT_MAPPED(self, self.OnMapped)

    def OnMenuHelpAboutMenu(self, event):
        event.Skip()

    def OnMenuFileOpenMenu(self, event):
        dlg = wx.FileDialog(self, "Choose a file", ".", "", "*.*")
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()

                # Set up the mapping parser
                self.map_stream = open(filename, 'rb')
                parser = Parser(inp=self.map_stream)
                self.record_mapper = StreamMapper()
                parser.addSink(self.record_mapper)
                material_mapper = MaterialMapper()
                parser.addSink(material_mapper)
                self.recordPositionList.record_mapper = self.record_mapper
                self.recordPositionList.material_mapper = material_mapper

                # Set up the viewing parser
                self.view_stream = open(filename, 'rb')
                self.view_parser = Parser(inp=self.view_stream)
                self.record_keeper = RecordKeeper()
                self.view_parser.addSink(self.record_keeper)
                self.view_parser.parse(1)

                # Parse the file in a separate thread
                self.mapper = MapperThread(self, parser)

        finally:
            dlg.Destroy()

    def OnMapped(self, event):
        if event.cancelled:
            self.statusBar.SetStatusText('%s... Cancelled!' % (
                self.statusBar.GetStatusText()))
        else:
            self.recordPositionList.SetItemCount(
                len(self.record_mapper.indexes))
            self.statusBar.SetStatusText('%s... Done' % (
                self.statusBar.GetStatusText()))

        if self.map_stream is not None:
            self.map_stream.close()
            self.map_stream = None
        self.mapper = None

    def OnMenuFileCloseMenu(self, event):
        self.recordPositionList.record_mapper = None
        self.recordPositionList.material_mapper = None
        self.view_stream.close()
        self.view_stream = None
        self.view_parser = None
        self.record_mapper = None

        self.recordPositionList.SetItemCount(0)
        self.recordPositionList.Refresh()
        self.recordViewList.SetItemCount(0)
        self.recordViewList.Refresh()

        if self.mapper:
            self.mapper.cancel()

    def OnMenuFileExitMenu(self, event):
        self.Close()

    def OnRecordPositionListListItemSelected(self, event):
        if self.record_mapper:
            self.view_stream.seek(self.record_mapper.indexes[event.GetIndex()])
            self.view_parser.parse(1)
            self.recordViewList.record = self.record_keeper.record_type, self.record_keeper.record_data
