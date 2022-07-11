import sys, pygame, grid
pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255

# in pixels
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# size of each cell
CELL_SIZE = 20

# width and height in number of cells
GRID_WIDTH, GRID_HEIGHT = 20, 20

# center the grid on the screen
GRID_X, GRID_Y = (SCREEN_WIDTH / 2) - (GRID_WIDTH * CELL_SIZE) / 2, (SCREEN_HEIGHT / 2) - 50 - (GRID_HEIGHT * CELL_SIZE) / 2

# create the displayable screen, its a surface that we can draw to
screen = pygame.display.set_mode((800, 600))
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    if not running: sys.exit()

    # clear the screen with black
    screen.fill(BLACK)

    grid.drawGrid(screen, WHITE, GRID_X, GRID_Y, GRID_WIDTH, 20, CELL_SIZE)

    # flush the buffer and display on the screen
    pygame.display.flip()
