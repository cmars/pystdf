
class RecordKeeper:
    def __init__(self):
        self.record_type = None
        self.record_data = None
        
    def after_begin(self, dataSource):
        self.record_type = None
        self.record_data = None
        
    def after_send(self, dataSource, data):
        self.record_type, self.record_data = data
    
    