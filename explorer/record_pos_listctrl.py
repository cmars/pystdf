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
    
    def OnGetItemText(self, item, col):
        if self.__record_mapper is not None:
            if col == 0:
                return '%08X' % (self.__record_mapper.indexes[item])
            elif col == 1:
                return self.__record_mapper.types[item].__class__.__name__
        return ''
    
