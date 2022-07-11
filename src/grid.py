import pygame

def drawGrid(surface, color, x, y, width, height, cell_size):
    # Draws the main game grid, takes parameters for the surface to draw to, color, x & y position, width, height and cell size
    for i in range(width + 1):
        pygame.draw.line( surface, color, (x + ( i * cell_size ), y), (x + (i * cell_size), y + (height * cell_size)))
        for j in range(height + 1):
            pygame.draw.line( surface, color, (x + ( i * cell_size ), y + ( j * cell_size )), (x + width * cell_size, y + (j * cell_size )))


