
class TableTemplate:
    def __init__(self, columnNames, columnTypes, name=None):
        if name is None:
            self.name = self.__module__ + '.' + self.__class__.__name__
        else:
            self.name = name
        self.columnNames = columnNames
        self.columnTypes = columnTypes


