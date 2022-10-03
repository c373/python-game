import sys, pygame, grid, snake, random, math, controls, ui

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
        self.h3 = pygame.font.Font("../assets/fonts/MirandaNbp-X242.ttf", 40)

        self.UI = {
            GameState.STARTMENU: [
                ui.Text("SNAKE GAME", [400, 300], self.h1, False, self.COLORS.WHITE),
                ui.Text("PRESS ENTER", [400, 350], self.h2, False, self.COLORS.RED),
            ],
            GameState.PAUSED: [
                ui.Text("PAUSED", [400, 300], self.h1, False, self.COLORS.WHITE),
                ui.Text("ENTER TO RESUME", [400, 350], self.h2, False, self.COLORS.RED),
            ],
            GameState.PLAYING: [
                ui.Text(
                    "ARROW KEYS OR  WASD TO MOVE",
                    [400, 475],
                    self.h3,
                    False,
                    self.COLORS.WHITE
                ),
                ui.Text(
                    "ENTER TO PAUSE",
                    [400, 515],
                    self.h3,
                    False,
                    self.COLORS.WHITE
                ),
                ui.Text(
                    "ESC TO EXIT",
                    [400, 555],
                    self.h3,
                    False,
                    self.COLORS.WHITE
                )
            ],
            GameState.GAMEOVER: [
                ui.Text(
                    "GAMEOVER",
                    [400, 300],
                    self.h1,
                    False,
                    self.COLORS.RED
                ),
                ui.Text(
                    "ENTER - RESET",
                    [400, 555],
                    self.h3,
                    False,
                    self.COLORS.WHITE
                ),
            ]
        }

        # necessary for tracking update frames
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 0

        self.resetGame()

    def resetGame(self) -> None:
        self.COLORS.WHITE = [192, 202, 245]
        self.player = snake.snake(
            [
                math.floor(self.GRID_WIDTH / 2),
                math.floor(self.GRID_HEIGHT / 2)
            ],
            self.CELL_SIZE,
            self.COLORS.WHITE
        )
        self.generateFood()


    def generateFood(self):
        while True:
            self.food = [
                random.randrange(0, self.GRID_WIDTH),
                random.randrange(0, self.GRID_HEIGHT)
            ]

            if not self.player.checkInSnake(self.food, False):
                break 

    def update(self, dt):

        for event in pygame.event.get():

            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.player.speed = True
            else:
                self.player.speed = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:
                    if self.state == GameState.STARTMENU:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.GAMEOVER:
                        self.state = GameState.PLAYING
                        self.resetGame()
                    pass

                if self.state == GameState.PLAYING:
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
            if (
                    self.player.nextLoc[0] < 0 or
                    self.player.nextLoc[1] < 0 or
                    self.player.nextLoc[0] >= self.GRID_WIDTH or
                    self.player.nextLoc[1] >= self.GRID_HEIGHT
                ):
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

        if self.state != GameState.STARTMENU:
            # draw the grid
            grid.drawGrid(
                pygame,
                self.screen,
                self.COLORS.WHITE,
                self.GRID_X, self.GRID_Y,
                self.GRID_WIDTH,
                self.GRID_HEIGHT,
                self.CELL_SIZE,
                self.DEBUG
            )

            # draw the food
            pygame.draw.rect(
                self.screen,
                self.COLORS.RED,
                pygame.Rect(
                    self.GRID_X + self.food[0] * self.CELL_SIZE,
                    self.GRID_Y + self.food[1] * self.CELL_SIZE,
                    self.CELL_SIZE, self.CELL_SIZE
                )
            )

            # draw the player snake
            self.player.draw(pygame, self.screen, self.GRID_X, self.GRID_Y)

        if self.state == GameState.PAUSED:
            pygame.draw.rect(
                self.screen,
                self.COLORS.BLACK,
                pygame.Rect(0, 0, 800, 600)
            )
        elif self.state == GameState.GAMEOVER:
            s = pygame.Surface((800,600))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill(self.COLORS.BLACK)           # this fills the entire surface
            self.screen.blit(s, (0,0))    # (0,0) are the top-left coordinates



        for text in self.UI[self.state]:
            text.draw(self.screen)

        # flush the buffer and display on the screen
        pygame.display.flip()


    def run(self):
        while True:

            self.dt = self.clock.tick(self.fps)/1000.0
            self.update(self.dt)
            self.draw()
