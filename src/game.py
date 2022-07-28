import sys, pygame, grid, snake, random

class game(object):
    class Colors:
        def __init__(self) -> None:
            self.BLACK = [0, 0, 0]
            self.WHITE = [255, 255, 255]
            self.RED = [255, 0, 0]

    def __init__(self) -> None:
        pygame.init()

        self.COLORS = self.Colors()

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

        # variables to manage game state
        self.running = True
        self.gameOver = False

        # necessary for tracking update frames
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

        # init player snake
        self.player = snake.snake([1, 1], self.CELL_SIZE)

        while True:
            self.food = [random.randrange(0, self.GRID_WIDTH), random.randrange(0, self.GRID_HEIGHT)]

            if self.food[0] != self.player.currentLoc[0] or self.food[1] != self.player.currentLoc[1]:
                break


    def update(self, dt):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.running == False:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.player.speed = True
            else:
                self.player.speed = False

            if not self.gameOver:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.direction = [0, -1]
                    if event.key == pygame.K_DOWN:
                        self.player.direction = [0, 1]
                    if event.key == pygame.K_LEFT:
                        self.player.direction = [-1, 0]
                    if event.key == pygame.K_RIGHT:
                        self.player.direction = [1, 0]

        if not self.gameOver:

            # check that the snake is not out of bounds
            if self.player.nextLoc[0] < 0 or self.player.nextLoc[1] < 0 or self.player.nextLoc[0] >= self.GRID_WIDTH or self.player.nextLoc[1] >= self.GRID_HEIGHT:
                # end game if true
                self.gameOver = True

            self.player.update(dt)


    def draw(self):
    
        # clear the screen with black
        self.screen.fill(self.COLORS.BLACK)
    
        # draw the grid
        grid.drawGrid(pygame, self.screen, self.COLORS.WHITE, self.GRID_X, self.GRID_Y, self.GRID_WIDTH, self.GRID_HEIGHT, self.CELL_SIZE)

        # draw the food
        pygame.draw.rect(self.screen, self.COLORS.RED, pygame.Rect(self.GRID_X + self.food[0] * self.CELL_SIZE, self.GRID_Y + self.food[1] * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # draw the player snake
        self.player.draw(pygame, self.screen, self.GRID_X, self.GRID_Y)
    
        # flush the buffer and display on the screen
        pygame.display.flip()


    def run(self):
        while self.running:
        
            self.dt = self.clock.tick(self.fps)/1000.0
            self.update(self.dt)
            self.draw()
