import random
import collections
import heapq

#grid = [[1 for i in range(d)] for i in range(d)]
d = 10 # size of grid
q = 0.5

# creates the grid
grid = [[0 for i in range(d)] for i in range(d)] # 0 signifies blocked, while 1 signifies open cell
openCells = []

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

# Returns if cell is in the grid
def validCell(x,y):
    return x >= 0 and x < d and y >= 0 and y < d

# print's grid in terminal
def printGrid():
     for x in range(d):
        for y in range(d):
            print(grid[x][y], end=" ")
        print("\n")

# initializes the grid with blocked cells
def init_grid():
    # open a random square in the grid
    start_x = random.randint(0, d - 1)
    start_y = random.randint(0, d - 1)
    grid[start_x][start_y] = 1
    openCells.append((start_x, start_y))

    # identify all blocked cells with exactly 1 open neighbor and randomly choose one of them to open
    oneOpenNeighbor = []
    for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
        if validCell(start_x + r, start_y + c):
            oneOpenNeighbor.append((start_x + r, start_y + c))

    while len(oneOpenNeighbor) != 0:
            randIndex = random.randint(0, len(oneOpenNeighbor) - 1)
            selected_x, selected_y = oneOpenNeighbor[randIndex]
            grid[selected_x][selected_y] = 1
            oneOpenNeighbor.remove((selected_x, selected_y))
            openCells.append((selected_x, selected_y))
            for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
                if validCell(selected_x + r, selected_y + c) and grid[selected_x + r][selected_y + c] == 0:
                    if (selected_x + r, selected_y + c) in oneOpenNeighbor:
                        oneOpenNeighbor.remove((selected_x + r, selected_y + c))
                    else:
                        oneOpenNeighbor.append((selected_x + r, selected_y + c))

    # identify all "dead end" cells
    deadend = []
    for x in range(d):
        for y in range(d):
            left, right, up, down = adjacent(x,y)
            if grid[x][y] == 1 and ((left != -1 and right == -1 and up == -1 and down == -1) or (left == -1 and right != -1 and up == -1 and down == -1) or (left == -1 and right == -1 and up != -1 and down == -1) or (left == -1 and right == -1 and up == -1 and down != -1)):
                deadend.append((x,y))

    # randomly open one closed neighbor of approximately half of the "dead end" cells
    half = len(deadend) // 1.75

    while len(deadend) > half:
        randIndex = random.randint(0, len(deadend) - 1)
        selected_x, selected_y = deadend[randIndex]
        neighbors = []
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(selected_x + r, selected_y + c) and grid[selected_x + r][selected_y + c] == 0:
                    neighbors.append((selected_x + r, selected_y + c))
        randNeighborIndex = random.randint(0, len(neighbors) - 1)
        neighborR, neighborC = neighbors[randNeighborIndex]
        grid[neighborR][neighborC] = 1
        openCells.append((neighborR, neighborC))
        deadend.remove((selected_x, selected_y))

fireCells = []
adjToFireCells = []

# resets lists
def reset(openCells, fireCells, adjToFireCells):
    openCells = []
    fireCells = []
    adjToFireCells = []

# initialize the bot, fire, and button cells 
def init_bot_fire_button():
    # randomly choose start location by randomly choosing open cells (bot is represented by 2)
    randIndex = random.randint(0, len(openCells) - 1)
    bot_x, bot_y = openCells[randIndex]
    grid[bot_x][bot_y] = 2
    openCells.remove((bot_x, bot_y))
    
    # start fire at random open cell (fire represented by 3)
    init_fire = random.randint(0, len(openCells) - 1) 
    fire_x, fire_y = openCells[init_fire]
    grid[fire_x][fire_y] = 3
    fireCells.append((fire_x,fire_y))
    for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
        if validCell(fire_x + r, fire_y + c) and grid[fire_x + r][fire_y + c] == 1:
            adjToFireCells.append((fire_x + r, fire_y + c))
    openCells.remove((fire_x, fire_y))

    # randomly choose button location by randomly choosing open cells (button is represented by 4)
    randIndex = random.randint(0, len(openCells) - 1)
    button_x, button_y = openCells[randIndex]
    grid[button_x][button_y] = 4
    openCells.remove((button_x, button_y))

    openCells.append((bot_x, bot_y))
    openCells.append((fire_x, fire_y))
    openCells.append((button_x, button_y))

    return bot_x, bot_y, button_x, button_y


# spread fire every time step based on the probability 1 - (1 - q)^k
def spread_fire():
    numChecked = 0
    currentCellsOnFire = len(fireCells)
    for cur_fire_x, cur_fire_y in fireCells:
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            fire_neighbor_x = cur_fire_x + r 
            fire_neighbor_y = cur_fire_y + c
            if validCell(fire_neighbor_x, fire_neighbor_y) and grid[fire_neighbor_x][fire_neighbor_y] == 1:
                k = 0
                for (r2,c2) in [(1,0), (-1,0), (0,-1), (0, 1)]:
                     if validCell(fire_neighbor_x + r2, fire_neighbor_y + c2) and (fire_neighbor_x + r2, fire_neighbor_y + c2) in fireCells:
                         k += 1
                spreadProb = (1 - pow((1 - q), k))
                setOnFire = random.uniform(0, 1) < spreadProb
                if setOnFire:
                    grid[fire_neighbor_x][fire_neighbor_y] = 3
                    fireCells.append((fire_neighbor_x, fire_neighbor_y))
                    # adjToFireCells.remove((fire_neighbor_x, fire_neighbor_y))
                    for (r2,c2) in [(1,0), (-1,0), (0,-1), (0, 1)]:
                        if validCell(fire_neighbor_x + r2, fire_neighbor_y + c2) and grid[fire_neighbor_x + r2][fire_neighbor_y + c2] == 1:
                            adjToFireCells.append((fire_neighbor_x + r2, fire_neighbor_y + c2))
        numChecked += 1
        if numChecked == currentCellsOnFire:
            break
                
# reconstruct path from bfs                        
def getPath(bot_x, bot_y, button_x, button_y, prev):
    path = []
    cur = (button_x, button_y)
    while cur != None:
        path.append((cur[0], cur[1]))
        cur = prev[cur[0]][cur[1]]

    path.reverse()
    start_x, start_y = path[0]
    if start_x == bot_x and start_y == bot_y:
        return path
    return []

# runs bfs starting from bot cell
def bfs(bot_x, bot_y):
    q = collections.deque()
    visited = []
    prev = [[None for i in range(d)] for i in range(d)]
    q.append((bot_x, bot_y))
    visited.append((bot_x, bot_y))

    while len(q) != 0:
        cur_x, cur_y = q.popleft()

        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (cur_x + r, cur_y + c) not in visited and (grid[cur_x + r][cur_y + c] == 1 or grid[cur_x + r][cur_y + c] == 4):
                q.append((cur_x + r, cur_y + c))
                visited.append((cur_x + r, cur_y + c))
                prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
    return prev

def printPrev(prev):
     for x in range(d):
        for y in range(d):
            print(prev[x][y], end=" ")
        print("\n")

# runs bot 1 
def run_bot_1():
    print("Running Bot 1")
    init_grid()
    bot_x, bot_y, button_x, button_y = init_bot_fire_button()
    prev = bfs(bot_x, bot_y)
    #printPrev(prev)
    path = getPath(bot_x, bot_y, button_x, button_y, prev)
    print(path)
    printGrid()
    time = 1
    while True:
        print("Time:" + str(time))
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[time]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire()
        printGrid()
        time += 1

# runs bot 2
def run_bot_2():
    print("Running Bot 2")
    init_grid()
    bot_x, bot_y, button_x, button_y = init_bot_fire_button()
    prev = bfs(bot_x, bot_y)
    #printPrev(prev)
    path = getPath(bot_x, bot_y, button_x, button_y, prev)
    print(path)
    printGrid()
    time = 1
    while True:
        print("Time:" + str(time))
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire()
        prev = bfs(bot_x, bot_y)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        print(path)
        printGrid()
        if len(path) == 0:
            return "Failed"
        time += 1

# runs updated bfs starting from bot cell to account for cells adjacent to current fire cells
def updated_bfs(bot_x, bot_y):
    q = collections.deque()
    visited = []
    prev = [[None for i in range(d)] for i in range(d)]
    q.append((bot_x, bot_y))
    visited.append((bot_x, bot_y))

    while len(q) != 0:
        cur_x, cur_y = q.popleft()

        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (cur_x + r, cur_y + c) not in visited and (cur_x + r, cur_y + c) not in adjToFireCells and (grid[cur_x + r][cur_y + c] == 1 or grid[cur_x + r][cur_y + c] == 4):
                q.append((cur_x + r, cur_y + c))
                visited.append((cur_x + r, cur_y + c))
                prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
    return prev

# runs bot 3
def run_bot_3():
    print("Running Bot 3")
    init_grid()
    bot_x, bot_y, button_x, button_y = init_bot_fire_button()
    prev = updated_bfs(bot_x, bot_y)
    #printPrev(prev)
    path = getPath(bot_x, bot_y, button_x, button_y, prev)
    if(path == []):
            prev = bfs(bot_x, bot_y)
            path = getPath(bot_x, bot_y, button_x, button_y, prev)
    print(path)
    printGrid()
    time = 1
    while True:
        print("Time:" + str(time))
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire()
        prev = updated_bfs(bot_x, bot_y)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        if(path == []):
            prev = bfs(bot_x, bot_y)
            path = getPath(bot_x, bot_y, button_x, button_y, prev)
        print(path)
        printGrid()
        if len(path) == 0:
            return "Failed"
        time += 1

# calculate heuristic based on manhatten distance
def h(x,y, button_x, button_y):
    return abs(x - button_x) + abs(y - button_y)

# runs A* starting from bot cell
def a_star(bot_x, bot_y, button_x, button_y):
    priority = []
    prev = [[None for i in range(d)] for i in range(d)]
    #distances = {[[-1 for i in range(d)] for i in range(d)]}
    distanceTo = {}

    heapq.heappush(priority, (0, (bot_x,bot_y)))
    distanceTo[(bot_x, bot_y)] = 0

    while len(priority) != 0:
        cur_x, cur_y = heapq.heappop(priority)[1]

        if grid[cur_x][cur_y] == 4:
            return prev
        
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (grid[cur_x + r][cur_y + c] == 1 or grid[cur_x + r][cur_y + c] == 4):
                temp_dist = distanceTo[(cur_x, cur_y)] + 1
                if (cur_x + r, cur_y + c) not in distanceTo or temp_dist < distanceTo[(cur_x + r, cur_y + c)]:
                    distanceTo[(cur_x + r, cur_y + c)] = temp_dist
                    prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
                    heapq.heappush(priority, (temp_dist + h(cur_x + r, cur_y + c, button_x, button_y), (cur_x + r, cur_y + c)))
                                   
               # temp_dist = distances[cur_x][cur_y] # need to finish
               # distanceTo[(cur_x, cur_y)] + h(cur_x + r, cur_y + c, button_x, button_y) < distanceTo[(cur_x + r, cur_y + c)])
               # prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
    



# runs bot 4
def run_bot_4(): 
    print("Running Bot 4")
    init_grid()
    bot_x, bot_y, button_x, button_y = init_bot_fire_button()
    prev = a_star(bot_x, bot_y, button_x, button_y)
    path = getPath(bot_x, bot_y, button_x, button_y, prev)
    print(path)
    printGrid()
    time = 1
    while True:
        print("Time:" + str(time))
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire()
        prev = a_star(bot_x, bot_y, button_x, button_y)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        print(path)
        printGrid()
        if len(path) == 0:
            return "Failed"
        time += 1


# runs all bots
def run_bots():
    # result = run_bot_1()
    # print("Task " + result)
    # reset(openCells, fireCells, adjToFireCells)
    # print("Reset")
    
    # result = run_bot_2()
    # print("Task " + result)
    # reset(openCells, fireCells, adjToFireCells)
    # print("Reset")

    # result = run_bot_3()
    # print("Task " + result)
    # reset(openCells, fireCells, adjToFireCells)
    # print("Reset") 

    result = run_bot_4()
    print("Task " + result)
    reset(openCells, fireCells, adjToFireCells)
    print("Reset") 


run_bots()