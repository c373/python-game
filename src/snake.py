import utils, math

class snake:

    nextLoc = [0, 0]
    currentLoc = [0, 0]
    direction = [1, 0]
    __color = [255, 255, 255]
    __moveInterval : float
    timeSinceLastMove : float
    CELL_SIZE : float

    def __init__(self, nextLoc, CELL_SIZE) -> None:
        self.speed = False
        self.nextLoc = nextLoc
        self.currentLoc = nextLoc[:]
        self.__moveInterval = 0.5
        self.moveInterval = 0.25
        self.timeSinceLastMove = 0
        self.CELL_SIZE = CELL_SIZE

    def update(self, dt):
        self.timeSinceLastMove += dt

        if self.speed:
           self.moveInterval = self.__moveInterval / 2
        else:
            self.moveInterval = self.__moveInterval

        if self.timeSinceLastMove > self.moveInterval:
            self.currentLoc = self.nextLoc[:]
            self.nextLoc[0] += self.direction[0]
            self.nextLoc[1] += self.direction[1]
            self.timeSinceLastMove = 0

    def draw(self, pygame, surface, x_offset, y_offset):

        pct = pow(self.timeSinceLastMove / self.moveInterval, 5)

        lerpedLoc = [
            utils.lerp(self.currentLoc[0], self.nextLoc[0], pct),
            utils.lerp(self.currentLoc[1], self.nextLoc[1], pct)
        ]

        # draw the nextLoc with filled white square
        # pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * self.nextLoc[0], y_offset + self.CELL_SIZE * self.nextLoc[1], self.CELL_SIZE, self.CELL_SIZE))

        # draw the nextLoc with a red square
        pygame.draw.rect(surface, [255, 0, 0], pygame.Rect(x_offset + self.CELL_SIZE * self.nextLoc[0], y_offset + self.CELL_SIZE * self.nextLoc[1], self.CELL_SIZE, self.CELL_SIZE), 1)

        # draw the lerpedLoc with a red square
        # pygame.draw.rect(surface, [255, 0, 0], pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE), 1)

        # draw the lerpedLoc with a filled white square
        pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE))

        # draw the lerpedLoc with a filled white square, rounded corners
        # pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE), 0, 7)
