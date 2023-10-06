import random

grid = []
d = 10 # size of grid

# creates the grid
for x in range(d):
    for y in range(d):
        grid[x][y] = 0 # 0 signifies empty, while 1 signifies open cell

# finds the open neighbors of a cell by finding coordinates left/right/up/down of given cell
def adjacent(x, y):
    if x > 0 and grid[x - 1][y] == 1:
        x_left = x - 1
    else:
        x_left = -1

    if x < len(grid) - 1 and grid[x + 1][y] == 1:
        x_right = x + 1
    else:
        x_right = -1
    
    if y > 0 and grid[x][y - 1] == 1:
        y_up = y - 1
    else: 
        y_up = -1
    
    if y < len(grid[x]) - 1 and grid[x][y + 1] == 1:
        y_down = y + 1
    else:
        y_down = -1

    return x_left, x_right, y_up, y_down

# open a random sqaure in the grid
random_x = random.randint(0, d - 1)
random_y = random.randint(0, d - 1)
grid[random_x][random_y] = 1


# identify all blocked cells with exactly 1 open neighbor and randomly choose one of them to open
possible = True
while possible:
    blocked = []
    for x in range(d):
        for y in range(d):
            left, right, up, down = adjacent(x,y)
            if (left != -1 and right == -1 and up == -1 and down == -1) or (left == -1 and right != -1 and up == -1 and down == -1) or (left == -1 and right == -1 and up != -1 and down == -1) or (left == -1 and right == -1 and up == -1 and down != -1):
                blocked.append([x,y])
    
    if len(blocked) == 0:
        break

    random_pick = random.randint(0, len(blocked) - 1)
    x1, y1 = blocked[random_pick]
    grid[x1][y1] = 1

# identify all "dead end" cells
deadend = []
for x in range(d):
    for y in range(d):
        left, right, up, down = adjacent(x,y)
        if grid[x][y] == 1 and ((left != -1 and right == -1 and up == -1 and down == -1) or (left == -1 and right != -1 and up == -1 and down == -1) or (left == -1 and right == -1 and up != -1 and down == -1) or (left == -1 and right == -1 and up == -1 and down != -1)):
            deadend.append([x,y])

# randomly open one closed neighbor of approximately half of the "dead end" cells
half = len(deadend) / 2

for i in half: