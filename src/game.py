import sys, pygame, grid, snake, random, math, controls

class game(object):
    DEBUG = False
    inputBuffer: controls.InputBuffer
    headlineFont: pygame.font.Font

    class Colors:
        def __init__(self) -> None:
            self.BLACK = [36, 37, 51]
            self.WHITE = [192, 202, 245]
            self.RED = [255, 102, 128]

    def __init__(self) -> None:
        pygame.init()

        self.COLORS = self.Colors()

        self.headlineFont = pygame.font.Font("../assets/fonts/MirandaNbp-X242.ttf", 32)
        self.title = self.headlineFont.render("00000", False, self.COLORS.WHITE)
        self.readme = self.headlineFont.render("NAVIGATION - WASD  OR  ARROW KEYS", False, self.COLORS.WHITE)

        # in pixels
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600

        # size of each cell
        self.CELL_SIZE = 20

        # width and height in number of cells
        self.GRID_WIDTH, self.GRID_HEIGHT = 20, 20

        # center the grid on the screen
        self.GRID_X = (self.SCREEN_WIDTH / 2) - (self.GRID_WIDTH * self.CELL_SIZE) / 2
        self.GRID_Y = (self.SCREEN_HEIGHT / 2) - 50 - (self.GRID_HEIGHT * self.CELL_SIZE) / 2

        # create the displayable screen, its a surface that we can draw to
        self.screen = pygame.display.set_mode((800, 600))

        # variables to manage game state
        self.running = True
        self.gameOver = False

        # necessary for tracking update frames
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

        # init the input buffer
        self.inputBuffer = controls.InputBuffer(controls.Direction.RIGHT)

        # init player snake
        self.player = snake.snake([math.floor(self.GRID_WIDTH / 2), math.floor(self.GRID_HEIGHT / 2)], \
                                  self.CELL_SIZE, \
                                  self.COLORS.WHITE, \
                                  self.inputBuffer
                                  )

        self.generateFood()

    def generateFood(self):
        while True:
            self.food = \
            [random.randrange(0, self.GRID_WIDTH), random.randrange(0, self.GRID_HEIGHT)]

            if not self.player.checkInSnake(self.food, False):
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
                        self.inputBuffer.push(controls.Direction.UP)

                    if event.key == pygame.K_DOWN:
                        self.inputBuffer.push(controls.Direction.DOWN)

                    if event.key == pygame.K_LEFT:
                        self.inputBuffer.push(controls.Direction.LEFT)

                    if event.key == pygame.K_RIGHT:
                        self.inputBuffer.push(controls.Direction.RIGHT)

        if not self.gameOver:

            # check that the snake is not out of bounds
            if \
                self.player.nextLoc[0] < 0 or \
                self.player.nextLoc[1] < 0 or \
                self.player.nextLoc[0] >= self.GRID_WIDTH or \
                self.player.nextLoc[1] >= self.GRID_HEIGHT:
                # self.player.checkInSnake(self.player.head.GetLocation(), True):

                # end game if true
                self.gameOver = True
                self.COLORS.WHITE = self.COLORS.RED

            if self.player.checkInSnake(self.food, False):
                self.player.grow()
                self.generateFood()

            self.inputBuffer.update()
            self.player.update(dt, self.inputBuffer)

    def draw(self):

        # clear the screen with black
        self.screen.fill(self.COLORS.BLACK)


        # draw the grid
        grid.drawGrid(pygame, \
                      self.screen, \
                      self.COLORS.WHITE, \
                      self.GRID_X, self.GRID_Y, \
                      self.GRID_WIDTH, \
                      self.GRID_HEIGHT, \
                      self.CELL_SIZE, \
                      self.DEBUG
                      )

        # draw the food
        pygame.draw.rect(self.screen, \
                         self.COLORS.RED, \
                         pygame.Rect(self.GRID_X + self.food[0] * self.CELL_SIZE, \
                                     self.GRID_Y + self.food[1] * self.CELL_SIZE, \
                                     self.CELL_SIZE, self.CELL_SIZE) \
                         )

        # draw the player snake
        self.player.draw(pygame, self.screen, self.GRID_X, self.GRID_Y)

        self.screen.blit(self.readme, [0,0])

        # flush the buffer and display on the screen
        pygame.display.flip()


    def run(self):
        while self.running:

            self.dt = self.clock.tick(self.fps)/1000.0
            self.update(self.dt)
            self.draw()
