import random

class CaveGenerator:
    
    WALL = "#"
    FLOOR = " "
    
    def __init__(self):
        self.SetCaveBorderWidth(2, 2)
        self.SetAdjacentRadius(1)
    
    def Generate(self, numColumns, numRows, percentage, smoothIterations):
        self.numRows = numRows
        self.numColumns = numColumns
        self.percentage = percentage
        
        self.GenerateRandomMap()
        
        for itr in range(smoothIterations):
           self.SmoothMap()
        
        return self.mapArray
    
    def GenerateRandomMap(self):
        self.mapArray = [[0 for x in range(self.numColumns)] for y in range(self.numRows)]
        
        for row in range(self.numRows):
            for column in range(self.numColumns):
                
                if self.IsOnBorder(row, column, self.GetCaveBorderWidthX(), self.GetCaveBorderWidthY()):
                    self.mapArray[row][column] = self.WALL
                    continue
                
                mapMiddle = self.numRows / 2
                    
                if row == mapMiddle:
                    self.mapArray[row][column] = self.FLOOR
                else:
                    self.mapArray[row][column] = self.RandomPercent()
                
        return self.mapArray
    
    def SmoothMap(self):
        for row in range(self.numRows):
            for column in range(self.numColumns):
                self.mapArray[row][column] = self.PlaceLogicWall(row, column)
    
    def PlaceLogicWall(self, row, column):
        numWalls = self.GetAdjacentWalls(row, column, self.GetAdjacentRadius(), self.GetAdjacentRadius())
        type = self.mapArray[row][column]
                
        if type == self.WALL:
            if numWalls >= 4:
                return self.WALL
            if numWalls < 2:
                return self.FLOOR
        else:
            if numWalls >= 5:
                return self.WALL
        
        return self.FLOOR
    
    def GetAdjacentWalls(self, row, column, scopeRow, scopeColumn):
        startRow = row - scopeRow
        startColumn = column - scopeColumn
        
        endRow = row + scopeRow
        endColumn = column + scopeColumn
        
        if startRow < 0: startRow = 0
        if startColumn < 0: startColumn = 0
        
        if endRow >= self.numRows: endRow = self.numRows - 1
        if endColumn >= self.numColumns: endColumn = self.numColumns - 1
        
        numWalls = 0
        for iRow in range(startRow, endRow + 1):
            for iColumn in range(startColumn, endColumn + 1):
                if iRow == row and iColumn == column:
                    continue
                if self.mapArray[iRow][iColumn] == self.WALL:
                    numWalls += 1
        
        return numWalls
    
    def IsOnBorder(self, row, column, scopeRow, scopeColumn):
        for i in range(scopeRow):
            if row == i or row == self.numRows - i - 1:
                return True
        for i in range(scopeColumn):
            if column == i or column == self.numColumns - i - 1:
                return True
        return False
    
    def RandomPercent(self):
        if self.percentage >= random.random():
            return self.WALL
        
        return self.FLOOR

    def PrintMap(self):
        
        for column in range(self.numColumns):
            for row in range(self.numRows):
                #reflected
                print(self.mapArray[row][column], end=" ")
            print()
        print()
    
    @staticmethod
    def PrintCustomMap(cave):
        numRows = len(cave)
        numColumns = len(cave[0])
        
        for row in range(numRows):
            for column in range(numColumns):   
                print(cave[row][column], end=" ")
            print()
        print()
    
    def SetCaveBorderWidth(self, xWidth, yWidth):
        self.caveBorderWidthX = xWidth
        self.caveBorderWidthY = yWidth
    def GetCaveBorderWidthX(self):
        return self.caveBorderWidthX
    def GetCaveBorderWidthY(self):
        return self.caveBorderWidthY
    
    def SetAdjacentRadius(self, newAdjacentRadius):
        self.adjacentRadius = newAdjacentRadius
    def GetAdjacentRadius(self):
        return self.adjacentRadius
