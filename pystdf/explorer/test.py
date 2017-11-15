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

import  wx
import  wx.grid as  gridlib

from pystdf.IO import Parser
from pystdf.Mapping import *
from pystdf.Writers import *

#---------------------------------------------------------------------------
class HugeTable(gridlib.PyGridTableBase):
    def __init__(self, record_mapper, f):
        gridlib.PyGridTableBase.__init__(self)
        self.record_mapper = record_mapper
        self.f = f

#        self.odd=gridlib.GridCellAttr()
#        self.odd.SetBackgroundColour("sky blue")
#        self.even=gridlib.GridCellAttr()
#        self.even.SetBackgroundColour("sea green")

#    def GetAttr(self, row, col, kind):
#        attr = [self.even, self.odd][row % 2]
#        attr.IncRef()
#        return attr

    # This is all it takes to make a custom data table to plug into a
    # wxGrid.  There are many more methods that can be overridden, but
    # the ones shown below are the required ones.  This table simply
    # provides strings containing the row and column values.

    def GetNumberRows(self):
        return len(self.record_mapper.indexes)

    def GetNumberCols(self):
        return 2

    def IsEmptyCell(self, row, col):
        return False

    value_getters = {
        0: lambda self, row: self.record_mapper.indexes[row],
        1: lambda self, row: self.record_mapper.types[row],
    }

    def GetValue(self, row, col):
        return self.value_getters[col](self, row)

    def SetValue(self, row, col, value):
        pass

#---------------------------------------------------------------------------
class HugeTableGrid(gridlib.Grid):
    def __init__(self, parent, record_mapper, f):
        gridlib.Grid.__init__(self, parent, -1)
        table = HugeTable(record_mapper, f)
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(table, True)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightDown)
    def OnRightDown(self, event):
        print("hello")
        print(self.GetSelectedRows())

#---------------------------------------------------------------------------
class TestFrame(wx.Frame):
    def __init__(self, parent, filename):
        f = open(filename, 'rb')
        p=Parser(inp=f)
        record_mapper = StreamMapper()
        p.addSink(record_mapper)

        print('Parsing %s...' % (filename))
        p.parse()
        print('Parse complete')

        wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640,480))
        grid = HugeTableGrid(self, record_mapper, f)
        grid.SetReadOnly(5,5, True)

#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None, sys.argv[1])
    frame.Show(True)
    app.MainLoop()
#---------------------------------------------------------------------------
