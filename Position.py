class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def GetRow(self): return self.row
    def GetColumn(self): return self.column
    def PrintPosition(self): print(self.row, self.column)