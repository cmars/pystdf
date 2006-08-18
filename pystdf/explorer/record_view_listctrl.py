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
    
