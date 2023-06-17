import pygame
from aStarAlgo import AStar
from pygame.locals import *
from user import User

class Grid:
    def __init__(self, width, height, square_size, gap):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.gap = gap
        self.screen = pygame.display.set_mode((width, height))
        self.colors = [[(255, 255, 255) for _ in range(width // (square_size + gap))] for _ in range(height // (square_size + gap))]
        pygame.init()
        self.mouse_down = False
        self.allowAdjustments = True
        self.rows = len(self.colors)  # Update based on colors list dimensions
        self.cols = len(self.colors[0])  # Update based on colors list dimensions
        self.default_value = 0
        self.start = (0, 0)
        self.end = (0, 0)
        self.grid = self.initialize_grid()
        self.aStar = AStar()
        self.user = User()
        self.user.startUp()
        self.closedList = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def initialize_grid(self):
        self.grid = [[self.default_value] * self.cols for _ in range(self.rows)]
        return self.grid

    def get_square_indices(self, x, y):
        col = x // (self.square_size + self.gap)
        row = y // (self.square_size + self.gap)
        return row, col
    
    def toggle_adjustments(self):
        self.allowAdjustments = not self.allowAdjustments
    
    def extractNodes(self, user):
        boardStartX = user.startX
        boardStartY = user.startY
        boardEndX = user.endX
        boardEndY = user.endY

        if user.startX == 50 or user.startY == 50:
            boardStartX = user.startX
            boardStartY = user.startY
            if user.startX == 50:
                boardStartX = 49
            
            if user.startY == 50:
                boardStartY = 49
            
        self.grid[boardStartX][boardStartY] = 1
        self.start = (boardStartX, boardStartY)

        if user.endX == 50 or user.endY == 50:
            boardEndX = user.endX
            boardEndY = user.endY
            if user.endX == 50:
                boardEndX = 49
            
            if user.endY == 50:
                boardEndY = 49
            
        self.grid[boardEndX][boardEndY] = 2
        self.end = (boardEndX, boardEndY)

    def update_color(self, row, col, color):
        self.colors[row][col] = color

    def draw_grid(self):
        for row in range(self.height // (self.square_size + self.gap)):
            for col in range(self.width // (self.square_size + self.gap)):
                x = col * (self.square_size + self.gap)
                y = row * (self.square_size + self.gap)
                pygame.draw.rect(self.screen, self.colors[row][col], (x, y, self.square_size, self.square_size))

        self.update_color(self.user.startX, self.user.startY, (0, 0, 255))
        self.update_color(self.user.endX, self.user.endY, (0, 0, 255))

        self.extractNodes(self.user)

    def setWalls(self, row, col):
        detectRow = row
        detectCol = col

        if row == 50 or col == 50:
            detectRow = row
            detectCol = col
            if row == 50:
                detectRow = 49

            if detectCol == 50:
                detectCol = 49

        self.grid[int(detectRow)][int(detectCol)] = 3  # Convert row and col to integers

    def get_node_value(self, x, y):
        print("getting node value")
        print(self.grid[int(x)][int(y)])  # Correct the indexing
            

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.toggle_adjustments()

                    if not self.allowAdjustments:
                        print("Running Algo")
                        self.aStar.runAlgo(self, self.start, self.end)

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = pygame.mouse.get_pos()
                    row, col = self.get_square_indices(x, y)
                    if self.allowAdjustments and 0 <= row < len(self.colors) and 0 <= col < len(self.colors[0]):
                        self.update_color(row, col, (0, 0, 0))  # Update the color of the clicked square to black
                        self.setWalls(row, col)
                        self.mouse_down = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_down = False
            elif event.type == MOUSEMOTION:
                if self.mouse_down:
                    x, y = pygame.mouse.get_pos()
                    row, col = self.get_square_indices(x, y)
                    if self.allowAdjustments and 0 <= row < len(self.colors) and 0 <= col < len(self.colors[0]):
                        self.update_color(row, col, (0, 0, 0))  # Update the color of the dragged square to black
                        self.setWalls(row, col)

        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()


