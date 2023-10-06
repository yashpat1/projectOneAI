import random

#grid = [[1 for i in range(d)] for i in range(d)]
d = 10 # size of grid
q = 0.5

# creates the grid
grid = [[0 for i in range(d)] for i in range(d)] # 0 signifies blocked, while 1 signifies open cell

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

#print's grid in terminal
def printGrid():
     for x in range(d):
        for y in range(d):
            print(grid[x][y], end=" ")
        print("\n")

# open a random square in the grid
start_x = random.randint(0, d - 1)
start_y = random.randint(0, d - 1)
grid[start_x][start_y] = 1

# identify all blocked cells with exactly 1 open neighbor and randomly choose one of them to open
oneOpenNeighbor = []
for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
    if start_x + r >= 0 and start_x + r < d and start_y + c >= 0 and start_y + c < d:
        oneOpenNeighbor.append((start_x + r, start_y + c))
while len(oneOpenNeighbor) != 0:
        randIndex = random.randint(0, len(oneOpenNeighbor) - 1)
        selected_x, selected_y = oneOpenNeighbor[randIndex]
        grid[selected_x][selected_y] = 1
        oneOpenNeighbor.remove((selected_x, selected_y))
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if selected_x + r >= 0 and selected_x + r < d and selected_y + c >= 0 and selected_y + c < d and grid[selected_x + r][selected_y + c] == 0:
                if (selected_x + r, selected_y + c) in oneOpenNeighbor:
                    oneOpenNeighbor.remove((selected_x + r, selected_y + c))
                else:
                    oneOpenNeighbor.append((selected_x + r, selected_y + c))
# possible = True
# while possible:
#     blocked = []
#     for x in range(d):
#         for y in range(d):
#             left, right, up, down = adjacent(x,y)
#             if (left != -1 and right == -1 and up == -1 and down == -1) or (left == -1 and right != -1 and up == -1 and down == -1) or (left == -1 and right == -1 and up != -1 and down == -1) or (left == -1 and right == -1 and up == -1 and down != -1):
#                 blocked.append([x,y])
    
#     if len(blocked) == 0:
#         break

    # random_pick = random.randint(0, len(blocked) - 1)
    # x1, y1 = blocked[random_pick]
    # grid[x1][y1] = 1

# identify all "dead end" cells
deadend = []
for x in range(d):
    for y in range(d):
        left, right, up, down = adjacent(x,y)
        if grid[x][y] == 1 and ((left != -1 and right == -1 and up == -1 and down == -1) or (left == -1 and right != -1 and up == -1 and down == -1) or (left == -1 and right == -1 and up != -1 and down == -1) or (left == -1 and right == -1 and up == -1 and down != -1)):
            deadend.append((x,y))

# randomly open one closed neighbor of approximately half of the "dead end" cells
half = len(deadend) // 2.5

while len(deadend) > half:
    randIndex = random.randint(0, len(deadend) - 1)
    selected_x, selected_y = deadend[randIndex]
    neighbors = []
    for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
                if selected_x + r >= 0 and selected_x + r < d and selected_y + c >= 0 and selected_y + c < d and grid[selected_x + r][selected_y + c] == 1:
                        neighbors.append((selected_x + r, selected_y + c))
    randNeighborIndex = random.randint(0, len(neighbors) - 1)
    neighborR, neighborC = neighbors[randNeighborIndex]
    grid[neighborR][neighborC] = 1
    deadend.remove((selected_x, selected_y))

#start 


# half = len(deadend) / 2.5

