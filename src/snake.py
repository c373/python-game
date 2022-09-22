import utils

class segment:
    _location = [0, 0]
    _lastLoc = [0, 0]

    def __init__(self, initLoc) -> None:
        self._location = initLoc[:]

    def GetLocation(self) -> list[int]:
        return self._location[:]

    def MoveBy(self, deltaLoc: list):
        self._lastLoc = self._location[:]
        self._location[0] = self._location[0] + deltaLoc[0]
        self._location[1] = self._location[1] + deltaLoc[1]

    def Follow(self, nextSeg):
        self._location = nextSeg.GetLocation()

    def draw(self, pygame, surface, x_offset, y_offset, cellSize, color) -> None:
        pygame.draw.rect(surface, \
                         color, \
                         pygame.Rect(x_offset + cellSize * self._location[0], \
                                     y_offset + cellSize * self._location[1], \
                                     cellSize, \
                                     cellSize \
                                     ) \
                         )

    def drawLerped(self, pygame, surface, x_offset, y_offset, cellSize, color, nextLoc, pct) -> None:
        lerpedLoc = [
            utils.lerp(self._lastLoc[0], self._location[0], pct),
            utils.lerp(self._lastLoc[1], self._location[1], pct)
        ]
        pygame.draw.rect(surface, color, pygame.Rect(x_offset + cellSize * self._location[0], y_offset + cellSize * self._location[1], cellSize, cellSize))

        # pygame.draw.rect(surface, color, pygame.Rect(x_offset + cellSize * self._lastLoc[0], y_offset + cellSize * self._lastLoc[1], cellSize, cellSize))

        # pygame.draw.rect(surface, color, pygame.Rect(x_offset + cellSize * lerpedLoc[0], y_offset + cellSize * lerpedLoc[1], cellSize, cellSize))


class snake:

    __color :list[int] = [255, 255, 255]
    nextLoc : list[int] = [0, 0]
    direction : list[int] = [1, 0]

    speed : bool
    __segments: list[segment]
    moveInterval: float
    timeSinceLastMove : float
    CELL_SIZE : float

    def __init__(self, initLoc: list, CELL_SIZE: float) -> None:
        self.nextLoc[0] = initLoc[0] + self.direction[0]
        self.nextLoc[1] = initLoc[1] + self.direction[1]

        self.speed = False
        self.__segments = [segment(initLoc)]
        self.__size = 0
        self.moveInterval = 0.5
        self.timeSinceLastMove = 0
        self.CELL_SIZE = CELL_SIZE
        

    def grow(self):
        self.__segments.append(segment(self.__segments[self.__size].GetLocation()))
        self.__size = self.__size + 1
        self.moveInterval -= utils.lerp(0.0, 0.0125, 1)

    def moveBy(self, deltaLoc: list):

        for i in range(self.__size, 0, -1):
            self.__segments[i].Follow(self.__segments[i - 1])

        self.__segments[0].MoveBy(deltaLoc)



    def checkInSnake(self, location) -> bool :
        for seg in self.__segments:
            if seg._location[0] == location[0] and seg._location[1] == location[1]:
                return True

        return False

    def update(self, dt) -> None:
        self.timeSinceLastMove += dt

        realMoveInterval = self.moveInterval / 2 if self.speed else self.moveInterval

        if self.timeSinceLastMove > realMoveInterval:
            self.nextLoc[0] = self.__segments[0]._location[0] + self.direction[0]
            self.nextLoc[1] = self.__segments[0]._location[1] + self.direction[1]
            self.moveBy(self.direction)
            self.timeSinceLastMove = 0

    def draw(self, pygame, surface, x_offset, y_offset) -> None:

        pct = pow(self.timeSinceLastMove / self.moveInterval, 5)

        for i in range(self.__size, 0, -1):
            self.__segments[i].draw(pygame, \
                     surface, \
                     x_offset, \
                     y_offset, \
                     self.CELL_SIZE, \
                     self.__color)

        self.__segments[0].drawLerped(pygame, \
                 surface, \
                 x_offset, \
                 y_offset, \
                 self.CELL_SIZE, \
                 self.__color, \
                 self.nextLoc, \
                 pct)

        # draw the nextLoc with filled white square
        # pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * self.nextLoc[0], y_offset + self.CELL_SIZE * self.nextLoc[1], self.CELL_SIZE, self.CELL_SIZE))

        # draw the nextLoc with a red square
        # pygame.draw.rect(surface, [255, 0, 0], pygame.Rect(x_offset + self.CELL_SIZE * self.nextLoc[0], y_offset + self.CELL_SIZE * self.nextLoc[1], self.CELL_SIZE, self.CELL_SIZE), 1)

        # draw the lerpedLoc with a red square
        # pygame.draw.rect(surface, [255, 0, 0], pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE), 1)

        # draw the lerpedLoc with a filled white square
        # pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE))

        # draw the lerpedLoc with a filled white square, rounded corners
        # pygame.draw.rect(surface, self.__color, pygame.Rect(x_offset + self.CELL_SIZE * lerpedLoc[0], y_offset + self.CELL_SIZE * lerpedLoc[1], self.CELL_SIZE, self.CELL_SIZE), 0, 7)
