import pygame

class Text:
    __baseFont: pygame.font.Font
    __lineSpacing: float
    position: list[float]
    __boundingRect: pygame.Rect
    __content: list[str]
    contentBuffer: list[str]
    __aa: bool
    __color: list[int]
    contentSurface: list[pygame.surface.Surface]

    def __init__(self, content: str, pos: list[float], font: pygame.font.Font, aa: bool, color: list[int]) -> None:
        self.__baseFont = font
        self.__lineSpacing = self.__baseFont.get_linesize()
        self.position = pos
        self.__content = content.splitlines()
        self.__aa = aa
        self.__color = color
        self.contentSurface = []

        for line in self.__content:
            self.contentSurface.append(self.__baseFont.render(line, self.__aa, self.__color))

        maxWidth = 0

        for surf in self.contentSurface:
            currentWidth = surf.get_bounding_rect().width
            if currentWidth > maxWidth:
                maxWidth = currentWidth

        self.__boundingRect = pygame.Rect(0, 0, maxWidth, len(self.__content) * self.__lineSpacing)

        self.position[0] -= self.__boundingRect.width / 2
        self.position[1] -= self.__boundingRect.height / 2

    def newTextToSurface(self, line: str) -> pygame.surface.Surface:
        return self.__baseFont.render(line, self.__aa, self.__color)

    # INCOMPLETE!! Cases where the __content and contentBuffer lists are not
    # not the same length are not handled correctly -- Needs work
    def update(self) -> None:
        currentSize = len(self.__content)
        for i in range(len(self.contentBuffer)):
            if  i > currentSize:
                self.__content.append(self.contentBuffer[i])
                self.contentSurface.append(self.newTextToSurface(self.contentBuffer[i]))
                continue

            if self.__content[i] != self.contentBuffer[i]:
                self.__content[i] = self.contentBuffer[i]
                self.contentSurface[i] = self.newTextToSurface(self.contentBuffer[i])

    def draw(self, dest: pygame.surface.Surface) -> None:
        for i in range(0, len(self.contentSurface)):
            dest.blit(self.contentSurface[i], [self.position[0], self.position[1] + i * self.__lineSpacing])
