class Direction:
    LEFT    = [-1, 0]
    UP      = [0, -1]
    RIGHT   = [1, 0]
    DOWN    = [0, 1]

class InputBuffer:
    mainBuffer: list[list[int]]
    MAX_SIZE: int = 3
    CURRENT_INDEX: int = 0
    TTL: float = 0.4
    __currentLife:float = 0.0
    UNFRESH: bool = True

    def __init__(self, initDirection: list[int]) -> None:
        self.mainBuffer = [initDirection]

    def update(self, dt: float):
        if not self.UNFRESH:
            self.__currentLife += dt
            if self.__currentLife >= self.TTL:
                self.__currentLife = 0.0
                self.UNFRESH = True

    def push(self, newDirection: list[int]):
        if self.UNFRESH:
            self.CURRENT_INDEX = 0
            self.mainBuffer.clear()
            print('buffer flushed')

        self.mainBuffer.insert(self.CURRENT_INDEX, newDirection)

        self.CURRENT_INDEX += 1
        self.UNFRESH = False

        if self.CURRENT_INDEX > self.MAX_SIZE:
            self.CURRENT_INDEX = 0
        self.DebugPrint()

    def pop(self) -> list[int]:
        if len(self.mainBuffer) <= 1:
            return self.mainBuffer[0]
        else:
            return self.mainBuffer.pop(0)

    def DebugPrint(self):
        print("CURRENT_INDEX", self.CURRENT_INDEX)
        for i in range(0, len(self.mainBuffer)):
            print(i, self.mainBuffer[i])
