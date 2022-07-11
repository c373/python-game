import sys, pygame, grid
pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255

screen = pygame.display.set_mode((800, 600))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(BLACK)

    grid.drawGrid(screen, WHITE, 20, 20, 20, 20, 20)

    pygame.display.flip()
