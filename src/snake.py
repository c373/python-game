import utils

class segment:
    _location = [0, 0]

    def __init__(self, initLoc) -> None:
        self._location = initLoc[:]

    def GetLocation(self) -> list[int]:
        return self._location[:]

    def move(self, nextSegmentLocation) -> None:
        self._location = nextSegmentLocation[:]

    def draw(self, pygame, surface, x_offset, y_offset, cellSize, color, nextLoc, pct) -> None:

        lerpedLoc = [
            utils.lerp(self._location[0], nextLoc[0], pct),
            utils.lerp(self._location[1], nextLoc[1], pct)
        ]

        # draw the lerpedLoc with a filled white square
        pygame.draw.rect(surface, \
                         color, \
                         pygame.Rect(x_offset + cellSize * lerpedLoc[0], \
                                     y_offset + cellSize * lerpedLoc[1], \
                                     cellSize, \
                                     cellSize \
                                     ) \
                         )


class snake:

    nextLoc = [0, 0]
    direction = [1, 0]
    __head : segment
    __segments: list[segment]
    __color = [255, 255, 255]
    __moveInterval : float
    timeSinceLastMove : float
    CELL_SIZE : float

    def __init__(self, nextLoc, CELL_SIZE) -> None:
        self.speed = False
        self.nextLoc = nextLoc
        self.__head = segment(nextLoc)
        self.__segments = []
        self.__moveInterval = 0.5
        self.moveInterval = 0.25
        self.timeSinceLastMove = 0
        self.CELL_SIZE = CELL_SIZE

    def grow(self):
        if len(self.__segments) == 0:
            self.__segments.append(segment(self.__head._location))
        else:
            self.__segments.append(segment(self.__segments[len(self.__segments)-1]._location))

    def checkInSnake(self, location) -> bool :
        if self.__head._location[0] == location[0] and self.__head._location[1] == location[1]:
            return True

        for seg in self.__segments:
            if seg._location[0] == location[0] and seg._location[1] == location[1]:
                return True

        return False

    def update(self, dt) -> None:
        self.timeSinceLastMove += dt

        if self.speed:
            self.moveInterval = self.__moveInterval / 2
        else:
            self.moveInterval = self.__moveInterval

        if self.timeSinceLastMove > self.moveInterval:
            self.__head.move(self.nextLoc)
            self.nextLoc[0] += self.direction[0]
            self.nextLoc[1] += self.direction[1]
            self.timeSinceLastMove = 0

    def draw(self, pygame, surface, x_offset, y_offset) -> None:

        pct = pow(self.timeSinceLastMove / self.moveInterval, 5)

        self.__head.draw(pygame, \
                         surface, \
                         x_offset, \
                         y_offset, \
                         self.CELL_SIZE, \
                         self.__color, \
                         self.nextLoc, \
                         pct)

        numSegments = len(self.__segments)

        for i in range(len(self.__segments)):
            self.__segments[i].draw(pygame, \
                                    surface, \
                                    x_offset, \
                                    y_offset, \
                                    self.CELL_SIZE, \
                                    self.__color, \
                                    self.__segments[utils.clamp(i+1, 0, numSegments)]._location, \
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
