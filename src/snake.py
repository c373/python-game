class snake:

    location = [0, 0]
    color = 255, 255, 255
    moveInterval : float
    timeSinceLastMove : float

    def __init__(self, location, CELL_SIZE) -> None:
        self.location = location
        self.moveInterval = 0.5
        self.timeSinceLastMove = 0
        self.CELL_SIZE = CELL_SIZE

    def update(self, direction, dt):
        # self.location[0] += direction[0] * self.moveInterval * dt
        # self.location[1] += direction[1] * self.moveInterval * dt
        self.timeSinceLastMove += dt

        if self.timeSinceLastMove > self.moveInterval:
            self.location[0] += direction[0]
            self.location[1] += direction[1]
            self.timeSinceLastMove = 0

    def draw(self, pygame, surface, x_offset, y_offset):
        pygame.draw.rect(surface, self.color, pygame.Rect(x_offset + self.CELL_SIZE * self.location[0], y_offset + self.CELL_SIZE * self.location[1], self.CELL_SIZE, self.CELL_SIZE))

