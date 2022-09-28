import utils, controls, os

class segment:
    _location = [0, 0]

    def __init__(self, initLoc) -> None:
        self._location = initLoc[:]

    def GetLocation(self) -> list[int]:
        return self._location[:]

    def draw(self, pygame, surface, x_offset, y_offset, cellSize, color) -> None:
        pygame.draw.rect(surface, \
                         color, \
                         pygame.Rect(x_offset + cellSize * self._location[0], \
                                     y_offset + cellSize * self._location[1], \
                                     cellSize, \
                                     cellSize \
                                     ) \
                         )

    def drawLerped(self, pygame, surface, x_offset, y_offset, cellSize, color, lastLoc, pct) -> None:
        lerpedLoc = [
            utils.lerp(self._location[0], lastLoc[0], pct),
            utils.lerp(self._location[1], lastLoc[1], pct),
        ]

        pygame.draw.rect(surface, color, pygame.Rect(x_offset + cellSize * lerpedLoc[0], y_offset + cellSize * lerpedLoc[1], cellSize, cellSize))


class snake:

    direction: list[int]
    nextLoc: list[int] = [0, 0]

    speed: bool
    grow: bool
    __segments: list[segment]
    __size: int
    __moveInterval: float
    __realMoveInterval: float
    timeSinceLastMove: float
    CELL_SIZE: float
    __color: list[int] = [255, 255, 255]

    def __init__(self, initLoc: list[int], CELL_SIZE: float, COLOR: list[int], inputBuffer: controls.InputBuffer) -> None:
        self.direction = controls.Direction.RIGHT
        self.nextLoc[0] = initLoc[0] + self.direction[0]
        self.nextLoc[1] = initLoc[1] + self.direction[1]

        self.speed = False
        self.grow = False
        self.__segments = [segment(initLoc)]
        self.__segments.append(segment([initLoc[0] - 1, initLoc[1]]))
        self.__segments.append(segment([initLoc[0] - 2, initLoc[1]]))
        self.__size = 2
        self.__moveInterval = 4.0
        self.__moveInterval = 0.5
        self.timeSinceLastMove = 0.0
        self.CELL_SIZE = CELL_SIZE
        self.__color = COLOR
        
    def checkInSnake(self, location: list[int], skipHead: bool) -> bool :
        start = 1 if skipHead else 0
        for i in range(start, self.__size):
            if self.__segments[i]._location[0] == location[0] and \
            self.__segments[i]._location[1] == location[1]:
                return True

        return False

    def update(self, dt: float) -> None:
        self.timeSinceLastMove += dt

        self.__realMoveInterval = self.__moveInterval / 2 if self.speed else self.__moveInterval

        if self.timeSinceLastMove > self.__realMoveInterval:
            self.nextLoc[0] = self.__segments[0]._location[0] + self.direction[0]
            self.nextLoc[1] = self.__segments[0]._location[1] + self.direction[1]
            self.__segments.insert(0, segment(self.nextLoc))

            if self.grow:
                self.__size = self.__size + 1
                self.__moveInterval -= utils.lerp(0.0, 0.0125, 1)
                self.grow = False
            else:
                self.__segments.pop()

            self.timeSinceLastMove = 0

            

    def draw(self, pygame, surface, x_offset, y_offset) -> None:

        pct = pow(self.timeSinceLastMove / self.__realMoveInterval, 5)

        r = self.__size - 1

        if self.grow:
            r += 1
        else:
            self.__segments[self.__size].drawLerped(pygame, \
                                          surface, \
                                          x_offset, \
                                          y_offset, \
                                          self.CELL_SIZE, \
                                          self.__color, \
                                          self.__segments[self.__size - 1].GetLocation(), \
                                          pct)

        for i in range(r, -1, -1):
            self.__segments[i].draw(pygame, \
                     surface, \
                     x_offset, \
                     y_offset, \
                     self.CELL_SIZE, \
                     self.__color)
