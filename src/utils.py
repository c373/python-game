# basic lerp function
# start - intial value
# end - final value
# pct - percentage (0-1)
def lerp(start:float, end:float, pct:float) -> float:
    return (start + (end - start) * pct)

def easeIn(t:float, e:float) -> float:
    return (pow(t, e))

def clamp(num, min, max):
    if num > max:
        return max
    elif num < min:
        return min

    return num

def colorWrap(num: int) -> int:
    if num > 255:
        return num - 256
    elif num < 0:
        return num + 256

    return num

def fadeColor(color: list[int], factor: int) -> list[int]:
    return [colorWrap(color[0] - factor), colorWrap(color[1] - factor), colorWrap(color[2] - factor)]
