grid = []
d = 10 # size of grid

for x in range(d):
    for y in range(d):
        grid[x][y] = 0 # 0 signifies empty, while 1 signifies open cell


def adjacent(x, y):
    if (x > 0):
        x_left = x - 1
    else:
        x_left = -1

    if (x < len(grid) - 1):
        x_right = x + 1
    else:
        x_right = -1
    
    if (y > 0):
        y_left = y - 1
    else: 
        y_left = -1
    
    if (y < len(grid[x]) - 1):
        y_right = y + 1
    else:
        y_right = -1
