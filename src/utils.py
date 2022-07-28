# basic lerp function
# start - intial value
# end - final value
# pct - percentage (0-1)
def lerp(start:float, end:float, pct:float) -> float:
    return (start + (end - start) * pct)

def easeIn(t:float, e:float) -> float:
    return (pow(t, e))
