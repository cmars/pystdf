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

class RecordViewListCtrl(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.__record_type, self.__record_data = None, None
    
    def get_record(self):
        return self.__record_type, self.__record_data
    def set_record(self, value):
        if value is None:
            self.__record_type, self.__record_data = None, None
            self.SetItemCount(0)
        else:
            self.__record_type, self.__record_data = value
            self.SetItemCount(len(self.__record_type.fieldNames))
            self.RefreshItems(0, len(self.__record_type.fieldNames)-1)
    record = property(get_record, set_record)
    
    def OnGetItemText(self, item, col):
        if col == 0 and self.__record_type is not None:
            return self.__record_type.fieldNames[item]
        elif col == 1 and self.__record_data is not None:
            return str(self.__record_data[item])
        return ''
    
