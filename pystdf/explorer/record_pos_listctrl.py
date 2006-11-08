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

class RecordPositionListCtrl(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.__record_mapper = None
    
    def get_record_mapper(self):
        return self.__record_mapper
    def set_record_mapper(self, value):
        self.__record_mapper = value
        if value is None:
            self.SetItemCount(0)
        else:
            self.SetItemCount(len(value.indexes))
    record_mapper = property(get_record_mapper, set_record_mapper)
    
    def get_material_mapper(self):
        return self.__material_mapper
    def set_material_mapper(self, value):
        self.__material_mapper = value
    material_mapper = property(get_material_mapper, set_material_mapper)
    
    def OnGetItemText(self, item, col):
        if self.__record_mapper is not None:
            if col == 0:
                return '%08X' % (self.__record_mapper.indexes[item])
            elif col == 1:
                return self.__record_mapper.types[item].__class__.__name__
            elif col == 2:
                return str(self.__material_mapper.waferid[item])
            elif col == 3:
                return str(self.__material_mapper.insertionid[item])
            elif col == 4:
                return str(self.__material_mapper.partid[item])
        return ''
    
