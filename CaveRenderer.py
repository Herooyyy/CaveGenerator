import pygame
import pygame.freetype
from decimal import Decimal

from CaveGenerator import CaveGenerator
from CaveCleaner import CaveCleaner
from Position import Position

# TODO:
#     > REPLACE "RENDER ONE SQUARE FOR EACH PIXEL" FOR A BUFFER IMAGE THAT WILL ONLY NEEDED TO BE RENDERED ONCE
#     > REMAKE OFFSET MOVEMENT WITH PROPER CAMERA SCALE AND SMOOTH MOVEMENT
#     > ADD UI CONTROLS TO GENERATE CAVES WITH DIFFERENT INPUTS
#     > SOLVE RELATION BETWEEN ROWS, COLUMNS AND X AND Y SO IT DOESNT REFLECT THE AXIS
    
class CaveRenderer:
    def init(self):
        self.setup()
        
        self.startGameLoop()
    
    def setup(self):
        self.SIZE = [1280, 720]
        pygame.init()
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Cave Renderer")
        self.done = False
        self.clock = pygame.time.Clock()
        self.gameFont = pygame.freetype.SysFont("Arial", 16)
    
    def startGameLoop(self):
        self.onStart()
        
        while not self.done:
            self.handleInput()
            
            self.update()
            
            self.render()
        
        if self.done:
            self.onQuit()
    
    #This method is called after setting up is done and before the main game loop starts
    #Used to set up game logic
    def onStart(self):
        print("STARTED SUCCESSFUL")
        
        self.caveGen = CaveGenerator()
        self.caveCl = CaveCleaner()

        self.GenerateCave()
        
        self.width = 10

    def GenerateCave(self):
        unprocessedCave = self.caveGen.Generate(72, 128, 0.5, 5)
        self.cave = self.caveCl.CleanCave(unprocessedCave, 100)
        self.caveGen.PrintMap()

    #Handles all input
    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_SPACE:
                    self.GenerateCave()
                
    #Updates all game logic before render is called
    def update(self):
        self.clock.tick(60)
    
    #Renders graphics to screen
    def render(self):
        self.screen.fill((255, 0, 0))
        
        self.RenderPolygons()
        
        pygame.display.flip()
    
    #Called right before the game loop ends and game closes
    def onQuit(self):
        pygame.quit()
    
    def RenderPolygons(self):
        for row in range(len(self.cave)):
            for column in range(len(self.cave[row])):
                form = self.CalculateForm(row, column)
                self.RenderPolygon(row * self.width,column * self.width,  form)
    
    def CalculateForm(self, row, column):
        topLeft = self.cave[row][column]
        
        if not self.IsInBounds(Position(row + 1, column)):
            topRight = CaveGenerator.FLOOR
        else:
            topRight = self.cave[row + 1][column]
            
        if not self.IsInBounds(Position(row + 1, column + 1)):
            bottomRight = CaveGenerator.FLOOR
        else:
            bottomRight = self.cave[row + 1][column + 1]
        
        if not self.IsInBounds(Position(row, column + 1)):
            bottomLeft = CaveGenerator.FLOOR
        else:
            bottomLeft = self.cave[row][column + 1]
        
        form = 0
        
        if topLeft == CaveGenerator.WALL:
            form += 1
        if topRight == CaveGenerator.WALL:
            form += 2
        if bottomLeft == CaveGenerator.WALL:
            form += 4
        if bottomRight == CaveGenerator.WALL:
            form += 8
        
        return form
    
    def RenderPolygon(self, offsetX, offsetY, form):
        width = self.width
        halfWidth = int((self.width/2))
        
        topLeft = (offsetX, offsetY)
        topRight = (width + offsetX, offsetY)
        bottomLeft = (offsetX, width + offsetY)
        bottomRight = (width + offsetX, width + offsetY)
        
        topCenter = (halfWidth + offsetX, offsetY)
        bottomCenter = (halfWidth + offsetX, width + offsetY)
        leftCenter = (offsetX, halfWidth + offsetY)
        rightCenter = (width + offsetX, halfWidth + offsetY)
        
        if form == 1:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topCenter, leftCenter]) #
        if form == 2:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topCenter, topRight, rightCenter]) #
        if form == 3:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topRight, rightCenter, leftCenter]) #
        if form == 4:
            pygame.draw.polygon(self.screen, (0, 0, 255), [leftCenter, bottomCenter, bottomLeft]) #
        if form == 5:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topCenter, bottomCenter, bottomLeft]) #
        if form == 6:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topCenter, topRight, rightCenter, bottomCenter, bottomLeft, leftCenter]) #
        if form == 7:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topRight, rightCenter, bottomCenter, bottomLeft]) #
        if form == 8:
            pygame.draw.polygon(self.screen, (0, 0, 255), [rightCenter, bottomRight, bottomCenter]) #
        if form == 9:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topCenter, rightCenter, bottomRight, bottomCenter, leftCenter])
        if form == 10:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topCenter, topRight, bottomRight, bottomCenter]) #
        if form == 11:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topRight, bottomRight, bottomCenter, leftCenter]) #
        if form == 12:
            pygame.draw.polygon(self.screen, (0, 0, 255), [leftCenter, rightCenter, bottomRight, bottomLeft]) #
        if form == 13:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topCenter, rightCenter, bottomRight, bottomLeft]) #
        if form == 14:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topCenter, topRight, bottomRight, bottomLeft, leftCenter])
        if form == 15:
            pygame.draw.polygon(self.screen, (0, 0, 255), [topLeft, topRight, bottomRight, bottomLeft]) #
    
    def IsInBounds(self, position):
        row = position.GetRow()
        column = position.GetColumn()
        
        if (row >= 0 and row < len(self.cave)) and (column >= 0 and column < len(self.cave[0])):
            return True
        return False