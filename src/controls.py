import os

class Direction:
    LEFT    = [-1, 0]
    UP      = [0, -1]
    RIGHT   = [1, 0]
    DOWN    = [0, 1]

class InputBuffer:
    mainBuffer: list[list[int]]
    MAX_SIZE: int = 2
    CURRENT_INDEX: int = 0

    def __init__(self, initDirection: list[int]) -> None:
        self.mainBuffer = [initDirection]

    def update(self):
        if self.CURRENT_INDEX >= self.MAX_SIZE:
            temp = self.mainBuffer[0].copy()
            self.mainBuffer.clear()
            self.mainBuffer.insert(0, temp)
            self.CURRENT_INDEX = 0

    def push(self, newDirection: list[int]):
        self.mainBuffer.insert(self.CURRENT_INDEX, newDirection)

        self.CURRENT_INDEX += 1


    def pop(self) -> list[int]:
        if len(self.mainBuffer) > 1:
            self.CURRENT_INDEX -= 1
            return self.mainBuffer.pop(0)
        else:
            return self.mainBuffer[0]

    def DebugPrint(self):
        os.system('clear')
        print("CURRENT_INDEX", self.CURRENT_INDEX)
        for i in range(0, len(self.mainBuffer)):
            print(i, self.mainBuffer[i])
