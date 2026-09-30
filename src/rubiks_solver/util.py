def char2num(c):
    if c == 'W':
        return 0
    elif c == 'R':
        return 4
    elif c == 'G':
        return 1
    elif c == 'O':
        return 5
    elif c == 'B':
        return 3
    elif c == 'Y':
        return 2
    else:
        return -1
def num2char(n):
    if n == 0:
        return 'W'
    elif n == 1:
        return 'G'
    elif n == 2:
        return 'Y'
    elif n == 3:
        return 'B'
    elif n == 4:
        return 'R'
    elif n == 5:
        return 'O'
    return 'W'
def color2bgr(color):
    if color == 'W':
        return (255, 255, 255)
    elif color == 'R':
        return (0, 0, 255)
    elif color == 'G':
        return (0, 255, 0)
    elif color == 'O':
        return (0, 165, 255)
    elif color == 'B':
        return (255, 0, 0)
    elif color == 'Y':
        return (0, 255, 255)
    return (255, 255, 255)