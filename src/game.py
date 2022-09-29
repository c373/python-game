import sys, pygame, grid, snake, random, math, controls, text_utils

class GameState:
    STARTMENU = 0,
    PLAYING = 1,
    PAUSED = 2,
    GAMEOVER = 3

class game(object):
    DEBUG = False
    headlineFont: pygame.font.Font
    state = GameState.STARTMENU
    UI: dict

    class Colors:
        def __init__(self) -> None:
            self.BLACK = [36, 37, 51]
            self.WHITE = [192, 202, 245]
            self.RED = [255, 102, 128]

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
        self.GRID_X = (self.SCREEN_WIDTH / 2) - (self.GRID_WIDTH * self.CELL_SIZE) / 2
        self.GRID_Y = (self.SCREEN_HEIGHT / 2) - 50 - (self.GRID_HEIGHT * self.CELL_SIZE) / 2

        # create the displayable screen, its a surface that we can draw to
        self.screen = pygame.display.set_mode((800, 600))

        self.h1 = pygame.font.Font("../assets/fonts/MirandaNbp-X242.ttf", 104)
        self.h2 = pygame.font.Font("../assets/fonts/MirandaNbp-X242.ttf", 64)

        self.UI = { \
            "STARTMENU": [ \
                text_utils.Text("PRESS ENTER", [400, 350], self.h2, False, self.COLORS.RED), \
                text_utils.Text("SNAKE GAME", [400, 250], self.h1, False, self.COLORS.WHITE), \
            ] \
        }

        # necessary for tracking update frames
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

        # init player snake
        self.player = snake.snake( \
                                  [ \
                                      math.floor(self.GRID_WIDTH / 2), \
                                      math.floor(self.GRID_HEIGHT / 2) \
                                  ], \
                                  self.CELL_SIZE, \
                                  self.COLORS.WHITE \
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.state == GameState.STARTMENU:
                    self.state = GameState.PLAYING

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.player.speed = True
            else:
                self.player.speed = False

            if self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.player.directionBuffer = controls.Direction.UP

                    if event.key == pygame.K_DOWN:
                        self.player.directionBuffer = controls.Direction.DOWN

                    if event.key == pygame.K_LEFT:
                        self.player.directionBuffer = controls.Direction.LEFT

                    if event.key == pygame.K_RIGHT:
                        self.player.directionBuffer = controls.Direction.RIGHT

        if self.state == GameState.PLAYING:

            # check that the snake is not out of bounds
            if \
                self.player.nextLoc[0] < 0 or \
                self.player.nextLoc[1] < 0 or \
                self.player.nextLoc[0] >= self.GRID_WIDTH or \
                self.player.nextLoc[1] >= self.GRID_HEIGHT:
                # self.player.checkInSnake(self.player.head.GetLocation(), True):

                # end game if true
                self.state = GameState.GAMEOVER
                self.COLORS.WHITE = self.COLORS.RED

            if self.player.checkInSnake(self.food, False):
                self.player.grow = True
                self.generateFood()

            self.player.update(dt)

    def draw(self):

        # clear the screen with black
        self.screen.fill(self.COLORS.BLACK)

        if self.state == GameState.STARTMENU:
            for uiText in self.UI["STARTMENU"]:
                uiText.draw(self.screen)
        else:
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

        # flush the buffer and display on the screen
        pygame.display.flip()


    def run(self):
        while True:

            self.dt = self.clock.tick(self.fps)/1000.0
            self.update(self.dt)
            self.draw()
