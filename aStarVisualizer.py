import pygame
from pygame.locals import *

class Visualizer:
    def __init__(self, width, height, square_size, gap):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.gap = gap
        self.screen = pygame.display.set_mode((width, height))
        self.colors = [[(255, 255, 255) for _ in range(width // (square_size + gap))] for _ in range(height // (square_size + gap))]
        pygame.init()
        self.mouse_down = False

    def update_color(self, row, col, color):
        self.colors[row][col] = color

    def get_square_indices(self, x, y):
        col = x // (self.square_size + self.gap)
        row = y // (self.square_size + self.gap)
        return row, col

    def draw_grid(self, user):
        for row in range(self.height // (self.square_size + self.gap)):
            for col in range(self.width // (self.square_size + self.gap)):
                x = col * (self.square_size + self.gap)
                y = row * (self.square_size + self.gap)
                pygame.draw.rect(self.screen, self.colors[row][col], (x, y, self.square_size, self.square_size))

        
        self.update_color(user.startX, user.startY, (0, 0, 255))  # Update the color of the square at row 2, column 3 to red
        self.update_color(user.endX, user.endY, (0, 0, 255))      # Update the color of the square at row 4, column 1 to blue

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = pygame.mouse.get_pos()
                    row, col = self.get_square_indices(x, y)
                    if 0 <= row < len(self.colors) and 0 <= col < len(self.colors[0]):
                        self.update_color(row, col, (0, 0, 0))  # Update the color of the clicked square to red
                        self.mouse_down = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_down = False
            elif event.type == MOUSEMOTION:
                if self.mouse_down:
                    x, y = pygame.mouse.get_pos()
                    row, col = self.get_square_indices(x, y)
                    if 0 <= row < len(self.colors) and 0 <= col < len(self.colors[0]):
                        self.update_color(row, col, (0, 0, 0))  # Update the color of the dragged square to red

        return True

    def run(self, user):
        running = True
        while running:
            running = self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw_grid(user)
            pygame.display.flip()

        pygame.quit()


