def drawGrid(pygame, surface, color, x, y, width, height, cell_size):
    # Draws the main game grid, takes parameters for the surface to draw to, color, x & y position, width, height and cell size
    for i in range(width):
        for j in range(height):
            pygame.draw.rect( surface, color, pygame.Rect(2 + x + i * cell_size, 2 + y + j * cell_size, cell_size - 4, cell_size - 4), 1)
