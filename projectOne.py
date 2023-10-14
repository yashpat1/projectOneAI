# Yash Patel, Siddh Parmar
# Each group member contributed fairly equally towards each method in the code (in which we shared ideas decided on the best course of action)

import random
import collections
import heapq

d = 35 # size of grid
q = 0.8
num_tests = 100


# finds the open neighbors of a cell by finding coordinates left/right/up/down of given cell
def adjacent(x, y, grid):
    numNeighbors = 0
    for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
        if validCell(x + r, y + c):
            numNeighbors += 1

    numBlockedNeighbors = 0
    for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
        if validCell(x + r, y + c) and grid[x + r][y + c] == 0:
            numBlockedNeighbors += 1

    return numNeighbors - numBlockedNeighbors == 1

# Returns if cell is in the grid
def validCell(x,y):
    return x >= 0 and x < d and y >= 0 and y < d

# initializes the grid with blocked cells
def init_grid(grid, openCells):
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
            if grid[x][y] == 1 and adjacent(x, y, grid):
                deadend.append((x, y))

    # randomly open one closed neighbor of approximately half of the "dead end" cells
    half = len(deadend) // 1.75

    while len(deadend) > half:
        randIndex = random.randint(0, len(deadend) - 1)
        selected_x, selected_y = deadend[randIndex]
        neighbors = []
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(selected_x + r, selected_y + c) and grid[selected_x + r][selected_y + c] == 0:
                    neighbors.append((selected_x + r, selected_y + c))
        if len(neighbors) == 0:
            deadend.remove((selected_x, selected_y))
            continue
        randNeighborIndex = random.randint(0, len(neighbors) - 1) #possible bug
        neighborR, neighborC = neighbors[randNeighborIndex]
        grid[neighborR][neighborC] = 1
        openCells.append((neighborR, neighborC))
        deadend.remove((selected_x, selected_y))

# initialize the bot, fire, and button cells 
def init_bot_fire_button(grid, openCells, fireCells, adjToFireCells):
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
        if validCell(fire_x + r, fire_y + c) and (grid[fire_x + r][fire_y + c] == 1 or grid[fire_x + r][fire_y + c] == 2):
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
def spread_fire1(grid, fireCells, adjToFireCells):
    adjCell_copy = []
    for adj_fire_x, adj_fire_y in adjToFireCells:
        adjCell_copy.append((adj_fire_x, adj_fire_y))

    for adj_fire_x, adj_fire_y in adjCell_copy:
        k = 0
        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(adj_fire_x + r, adj_fire_y + c) and (adj_fire_x + r, adj_fire_y + c) in fireCells:
                k += 1
        spreadProb = (1 - pow((1 - q), k))
        setOnFire = random.uniform(0, 1) < spreadProb
        if setOnFire:
            grid[adj_fire_x][adj_fire_y] = 3
            fireCells.append((adj_fire_x, adj_fire_y))
            adjToFireCells.remove((adj_fire_x, adj_fire_y))
            for (r2,c2) in [(1,0), (-1,0), (0,-1), (0, 1)]:
                if validCell(adj_fire_x + r2, adj_fire_y + c2) and (adj_fire_x + r2, adj_fire_y + c2) not in adjToFireCells and (grid[adj_fire_x + r2][adj_fire_y + c2] == 1 or grid[adj_fire_x + r2][adj_fire_y + c2] == 2 or grid[adj_fire_x + r2][adj_fire_y + c2] == 4):
                    adjToFireCells.append((adj_fire_x + r2, adj_fire_y + c2))

                
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
def bfs(bot_x, bot_y, grid):
    q = collections.deque()
    visited = []
    prev = [[None for i in range(d)] for i in range(d)]
    q.append((bot_x, bot_y))
    visited.append((bot_x, bot_y))

    while len(q) != 0:
        cur_x, cur_y = q.popleft()

        if grid[cur_x][cur_y] == 4:
            return prev

        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (cur_x + r, cur_y + c) not in visited and (grid[cur_x + r][cur_y + c] == 1 or grid[cur_x + r][cur_y + c] == 4):
                q.append((cur_x + r, cur_y + c))
                visited.append((cur_x + r, cur_y + c))
                prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
    return prev

# runs bot 1 
def run_bot_1():
    grid = [[0 for i in range(d)] for i in range(d)] # 0 signifies blocked, while 1 signifies open cell
    openCells = []
    fireCells = []
    adjToFireCells = []
    init_grid(grid, openCells)
    bot_x, bot_y, button_x, button_y = init_bot_fire_button(grid, openCells, fireCells, adjToFireCells)
    prev = bfs(bot_x, bot_y,grid)
    path = getPath(bot_x, bot_y, button_x, button_y, prev)
    time = 1
    while True:
        if len(path) == 0:
            return "Failed"
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[time]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire1(grid, fireCells, adjToFireCells)
        if grid[bot_x][bot_y] == 3 or grid[button_x][button_y] == 3:
            return "Failed"
        time += 1

# runs bot 2
def run_bot_2():
    grid = [[0 for i in range(d)] for i in range(d)] # 0 signifies blocked, while 1 signifies open cell
    openCells = []
    fireCells = []
    adjToFireCells = []
    init_grid(grid, openCells)
    bot_x, bot_y, button_x, button_y = init_bot_fire_button(grid, openCells, fireCells, adjToFireCells)
    time = 1
    while True:
        prev = bfs(bot_x, bot_y, grid)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        if len(path) == 0:
            return "Failed"
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire1(grid, fireCells, adjToFireCells)
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        time += 1

# runs updated bfs starting from bot cell to account for cells adjacent to current fire cells
def updated_bfs(bot_x, bot_y, grid, adjToFireCells):
    q = collections.deque()
    visited = []
    prev = [[None for i in range(d)] for i in range(d)]
    q.append((bot_x, bot_y))
    visited.append((bot_x, bot_y))

    while len(q) != 0:
        cur_x, cur_y = q.popleft()

        if grid[cur_x][cur_y] == 4:
            return prev

        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (cur_x + r, cur_y + c) not in visited and (cur_x + r, cur_y + c) not in adjToFireCells and (grid[cur_x + r][cur_y + c] == 1 or grid[cur_x + r][cur_y + c] == 4):
                q.append((cur_x + r, cur_y + c))
                visited.append((cur_x + r, cur_y + c))
                prev[cur_x + r][cur_y + c] = (cur_x, cur_y)
    return prev

# runs bot 3 using updated bfs
def run_bot_3():
    grid = [[0 for i in range(d)] for i in range(d)]
    openCells = []
    fireCells = []
    adjToFireCells = []
    init_grid(grid, openCells)
    bot_x, bot_y, button_x, button_y = init_bot_fire_button(grid, openCells, fireCells, adjToFireCells)
    time = 1
    while True:
        prev = updated_bfs(bot_x, bot_y, grid, adjToFireCells)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        if(path == []):
            prev = bfs(bot_x, bot_y, grid)
            path = getPath(bot_x, bot_y, button_x, button_y, prev)
        if len(path) == 0:
            return "Failed"
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire1(grid, fireCells, adjToFireCells)
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        time += 1

# calculate heuristic based on manhatten distance
def h(x, y, button_x, button_y):
    return abs(x - button_x) + abs(y - button_y)

# calculate the weight based on the distance of a neighboring cell to its nearest fire cell
def weight(x, y, grid):
    q = collections.deque()
    visited = []
    distanceTo = {}
    q.append((x, y))
    visited.append((x, y))
    distanceTo[(x,y)] = 0

    while len(q) != 0:
        cur_x, cur_y = q.popleft()

        if grid[cur_x][cur_y] == 3:
            return 1 / distanceTo[(cur_x, cur_y)]

        for (r,c) in [(1,0), (-1,0), (0,-1), (0, 1)]:
            if validCell(cur_x + r, cur_y + c) and (cur_x + r, cur_y + c) not in visited and (grid[cur_x + r][cur_y + c] != 0):
                q.append((cur_x + r, cur_y + c))
                visited.append((cur_x + r, cur_y + c))
                distanceTo[(cur_x + r, cur_y + c)] = distanceTo[(cur_x, cur_y)] + 1
                
    return 0
     

# runs A* starting from bot cell
def a_star(bot_x, bot_y, button_x, button_y, grid):
    priority = []
    prev = [[None for i in range(d)] for i in range(d)]
    distanceTo = {}
    weights = {}
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
                    if (cur_x + r, cur_y + c) not in weights:
                        cellWeight = weight(cur_x + r, cur_y + c, grid)
                        weights[(cur_x + r, cur_y + c)] = cellWeight
                    heapq.heappush(priority, (temp_dist +  weights[(cur_x + r, cur_y + c)] + h(cur_x + r, cur_y + c, button_x, button_y), (cur_x + r, cur_y + c)))
    return prev

# runs bot 4
def run_bot_4(): 
    grid = [[0 for i in range(d)] for i in range(d)]
    openCells = []
    fireCells = []
    adjToFireCells = []
    init_grid(grid, openCells)
    bot_x, bot_y, button_x, button_y = init_bot_fire_button(grid, openCells, fireCells, adjToFireCells)
    time = 1
    while True:
        prev = a_star(bot_x, bot_y, button_x, button_y, grid)
        path = getPath(bot_x, bot_y, button_x, button_y, prev)
        if len(path) == 0:
            return "Failed"
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 1
        bot_x, bot_y = path[1]
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        grid[bot_x][bot_y] = 2
        if bot_x == button_x and bot_y == button_y:
            return "Completed"
        spread_fire1(grid, fireCells, adjToFireCells)
        if grid[bot_x][bot_y] == 3:
            return "Failed"
        time += 1


# runs all bots
def run_bots():
    # 0.2, 0.4, 0.6, 0.8 
    print()
    num_success = 0
    num_fail = 0
    print("Running Tests for Bot 1 at q: " + str(q))
    for i in range(num_tests):
        result = run_bot_1()
        if result == "Completed":
            num_success += 1
        else:
            num_fail += 1
    print(str(num_success) + "/" + str(num_tests) + " PASS")
    print(str(num_fail) + "/" + str(num_tests) + " FAIL")

    print()
    num_success = 0
    num_fail = 0
    print("Running Tests for Bot 2 at q: " + str(q))
    for i in range(num_tests):
        result = run_bot_2()
        if result == "Completed":
            num_success += 1
        else:
            num_fail += 1
    print(str(num_success) + "/" + str(num_tests) + " PASS")
    print(str(num_fail) + "/" + str(num_tests) + " FAIL")

    print()
    num_success = 0
    num_fail = 0
    print("Running Tests for Bot 3 at q: " + str(q))
    for i in range(num_tests):
        result = run_bot_3()
        if result == "Completed":
            num_success += 1
        else:
            num_fail += 1
    print(str(num_success) + "/" + str(num_tests) + " PASS")
    print(str(num_fail) + "/" + str(num_tests) + " FAIL")

    print()
    num_success = 0
    num_fail = 0
    print("Running Tests for Bot 4 at q: " + str(q))
    for i in range(num_tests):
        result = run_bot_4()
        if result == "Completed":
            num_success += 1
        else:
            num_fail += 1
    print(str(num_success) + "/" + str(num_tests) + " PASS")
    print(str(num_fail) + "/" + str(num_tests) + " FAIL")

run_bots()