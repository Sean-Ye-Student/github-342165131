import random
sizeX, sizeY = 200, 200
startX, startY = 0, 0
endX, endY = 0, 0
inf = 10**6
while startX == endX and startY == endY:
    startX, startY = (random.randint(0, sizeX - 1), random.randint(0, sizeY - 1))
    endX, endY = (random.randint(0, sizeX - 1), random.randint(0, sizeY - 1))
wall_chance = 25
grid, grid2 = [[[(False if random.randint(0, 100) <= wall_chance else True), inf] for x in range(sizeX)] for y in range(sizeY)], []
grid[startY][startX] = [True, 0]
grid[endY][endX] = [True, inf]
square_size = 100, 100
def setup():
    global square_size
    size(1000, 1000)
    square_size = min(int(width/sizeX), int(height/sizeY))

queue, queue2 = [(startX, startY)], [(startX, startY)]
valid_pos = lambda cx, cy, x, y: (cx != x or cy != y) and (abs(cx) - abs(x) == 0 or abs(cy) - abs(y) == 0) and cx + cy != 0 and 0 <= x < sizeX and 0 <= y < sizeY and grid[y][x][0] == True

def DFS(queue, grid, fast):
    cx, cy = map(int, queue[0])
    tx, ty, td = -1, -1, -1
    lowest_pd = inf
    for x in range(cx - 1, cx + 2):
        for y in range(cy - 1, cy + 2):
            if valid_pos(cx, cy, x, y):
                pd = ((endX - x)**2 + (endY - y)**2) ** 0.5
                print(grid[cy][cx][1], grid[y][x][1])
                d, d2 = grid[cy][cx][1], grid[y][x][1]
                if x == endX and y == endY:
                    grid[endY][endX][1] = d + 1
                    return queue, grid
                
                if d + 1 < d2 and pd < lowest_pd:
                    tx, ty, td = x, y, d + 1
                    lowest_pd = pd
    if tx > -1 and ty > -1 and td > -1:
        grid[ty][tx][1] = d + 1
        if fast:
            queue = [(tx,ty)] + queue
        else:
            queue.append((tx,ty))
    else:
        queue.pop(0)
    return queue, grid

def draw():
    global queue, queue2, grid, grid2
    if len(queue) < 1:
        return
    # for y, row in enumerate(grid):
    #     for x, state in enumerate(row):
    #         if x == startX and y == startY:
    #             fill(0, 255, 0)
    #         elif x == endX and y == endY:
    #             fill(255, 0, 0)
    #         elif state[0]:
    #             if state[1] == inf:
    #                 fill(255, 255, 255)
    #             else:
    #                 distance = ((endX - startX)**2 + (endY - startY)**2) ** 0.5
    #                 fill(0, 255 * distance/state[1], 255)
    #         else:
    #             fill(0,0,0)
    #         rect(x * square_size, y * square_size, square_size, square_size)
    
    if grid[endY][endX][1] < inf:
        for pos in queue:
            fill(0,255,0)
            rect(pos[0] * square_size, pos[1] * square_size, square_size, square_size)
        
        # if len(grid2) < 1:
        #     grid2 = [[[False, inf] for x in range(sizeX)] for y in range(sizeY)]
        #     grid2[startY][startX] = [True, 0]
        #     grid2[endY][endX] = [True, inf]
        #     for pos in queue:
        #         grid2[pos[1]][pos[0]] = True

        # for y, row in enumerate(grid2):
        #     for x, state in enumerate(row):
        #         print(type(state), "its true" if state else "false", state, state[0])
        #         if x == startX and y == startY:
        #             fill(0, 255, 0)
        #         elif x == endX and y == endY:
        #             fill(255, 0, 0)
        #         elif state[0]:
        #             if state[1] == inf:
        #                 fill(255, 255, 255)
        #             else:
        #                 distance = ((endX - startX)**2 + (endY - startY)**2) ** 0.5
        #                 fill(0, 255 * distance/state[1], 255)
        #         else:
        #             fill(0,0,0)
        #         rect(x * square_size, y * square_size, square_size, square_size)
        
        # queue2, grid2 = DFS(queue2, grid2, True)
        return

    queue, grid = DFS(queue, grid, True)
