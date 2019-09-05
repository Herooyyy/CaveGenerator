from CaveGenerator import CaveGenerator
from Position import Position


class CaveCleaner:
    def CleanCave(self, caveArray, lowerThreshold):
        self.caveArray = caveArray
        self.numRows = len(self.caveArray)
        self.numColumns = len(self.caveArray[0])
        
        self.lowerThreshold = lowerThreshold
        self.acceptedCaves = []
        
        index = 0
        for row in range(self.numRows):
            for column in range(self.numColumns):
                if self.caveArray[row][column] == CaveGenerator.FLOOR:
                    self.placesToCheck = []
                    position = Position(row, column)
                    self.character = chr(65 + index)
                    self.CategorizePosition(position)
                    index += 1
        
        self.FillHoles()
        
        return self.caveArray
                    
    def PrintMap(self):  
        print("")
        for row in range(self.numRows):
            for column in range(self.numColumns):
                if self.caveArray[row][column] == CaveGenerator.WALL:
                    print(" ", end=" ")
                else:
                    print(self.caveArray[row][column], end=" ")
            print()
    
    def IsWall(self, position):
        if self.IsInMap(position) and self.caveArray[position.GetRow()][position.GetColumn()] == CaveGenerator.WALL:
            return True
        return False
    
    def IsSameIndex(self, position):
        row = position.GetRow()
        column = position.GetColumn()
        
        if self.caveArray[row][column] == self.character:
            return True
        return False
    
    def CategorizePosition(self, position):
        self.currentNumber = 0
        self.SetCharacterOnPosition(position)
        
        self.AddAdjacentPlaces(position)
        
        while self.placesToCheck.__len__() > 0:
            for place in self.placesToCheck:
                self.SetCharacterOnPosition(place)  
                self.AddAdjacentPlaces(place)
                self.placesToCheck.remove(place)
        
        if self.currentNumber >= self.lowerThreshold:
            self.acceptedCaves.append(self.character)
            
    
    def FillHoles(self):
        for row in range(self.numRows):
            for column in range(self.numColumns):
                if self.acceptedCaves.count(self.caveArray[row][column]) == 0:
                    self.caveArray[row][column] = CaveGenerator.WALL
                else:
                    self.caveArray[row][column] = CaveGenerator.FLOOR
        
    def AddAdjacentPlaces(self, position):
        row = position.GetRow()
        column = position.GetColumn()
        
        top = Position(row + 1, column)
        bottom = Position(row - 1, column)
        left = Position(row, column - 1)
        right = Position(row, column + 1)
        
        self.AddPlace(right)
        self.AddPlace(bottom)
        self.AddPlace(left)
        self.AddPlace(top)
    
    def AddPlace(self, position):
        if self.IsInMap(position) and not self.IsWall(position) and not self.IsSameIndex(position):
            self.placesToCheck.append(position)
    
    def SetCharacterOnPosition(self, position):
        self.caveArray[position.GetRow()][position.GetColumn()] = self.character
        self.currentNumber += 1
        
    def IsInMap(self, position):
        if position.GetRow() >= 0 and position.GetRow() < self.numRows and position.GetColumn() >= 0 and position.GetColumn() < self.numColumns:
            return True
