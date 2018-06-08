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

class RecordPositionTable(gridlib.PyGridTableBase): 
    def __init__(self, record_mapper): 
        gridlib.PyGridTableBase.__init__(self) 
        self.record_mapper = record_mapper
        
    def GetNumberRows(self):
        print('GetNumberRows: %d' % (len(self.record_mapper.indexes)))
        return len(self.record_mapper.indexes)
    
    def GetNumberCols(self): 
        return 2
    
    col_names = {
        0:'File Offset (Hex)', 
        1:'Record Type',
    }
    def GetColLabelValue(self, col):
        return self.col_names[col]
    
    def IsEmptyCell(self, row, col):
        return False 
    
    value_getters = {
        0:lambda self, row: '%08X' % (self.record_mapper.indexes[row]),
        1:lambda self, row: self.record_mapper.types[row].__class__.__name__,
    }
    
    def GetValue(self, row, col):
        return self.value_getters[col](self, row)
    
    def SetValue(self, row, col, value): 
        pass

