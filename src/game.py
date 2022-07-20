import sys, pygame, grid, snake
from pygame.constants import CONTROLLER_AXIS_INVALID

class game(object):
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

        self.BLACK = 0, 0, 0
        self.WHITE = 255, 255, 255

        # in pixels
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600

        # size of each cell
        self.CELL_SIZE = 20

        # width and height in number of cells
        self.GRID_WIDTH, self.GRID_HEIGHT = 20, 20

        # center the grid on the screen
        self.GRID_X, self.GRID_Y = (self.SCREEN_WIDTH / 2) - (self.GRID_WIDTH * self.CELL_SIZE) / 2, (self.SCREEN_HEIGHT / 2) - 50 - (self.GRID_HEIGHT * self.CELL_SIZE) / 2

        # create the displayable screen, its a surface that we can draw to
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.direction = [1, 0]

        self.player = snake.snake([1, 1], self.CELL_SIZE)


    def update(self, direction, dt):

        for event in pygame.event.get():
            if event.type == pygame.QUIT | self.running == False:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    self.direction = [0, -1]
                if event.key == pygame.K_DOWN:
                    self.direction = [0, 1]
                if event.key == pygame.K_LEFT:
                    self.direction = [-1, 0]
                if event.key == pygame.K_RIGHT:
                    self.direction = [1, 0]

        self.player.update(direction, dt)



    def draw(self):
    
        # clear the screen with black
        self.screen.fill(self.BLACK)
    
        grid.drawGrid(pygame, self.screen, self.WHITE, self.GRID_X, self.GRID_Y, self.GRID_WIDTH, 20, self.CELL_SIZE)
        self.player.draw(pygame, self.screen, self.GRID_X, self.GRID_Y)
    
        # flush the buffer and display on the screen
        pygame.display.flip()


    def run(self):
        while self.running:
        
            self.dt = self.clock.tick(self.fps)/1000.0
            self.update(self.direction, self.dt)
            self.draw()
