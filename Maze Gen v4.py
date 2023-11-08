import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from collections import deque
import time
import matplotlib.pyplot as plt 
import psutil

date = time.ctime()
start = time.perf_counter()
#---------Parameters-----------

#Inital size
height = width = 50
#Number of mazes
sizes = 30
#Increment to the size
increment = 5

#Note: Final size = Inital size + sizes*Increment

sleep = False
printNum = True
plotit = True
log = True

# Function to get neighbors of a cell
def get_neighbors(maze, cell):
    row, col = cell
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
    
    neighbors = []
    
    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != 'w':
            neighbors.append((r, c))
    
    return neighbors

# BFS algorithm to find a path to the exit
def bfs_solver(maze, start, end):
    queue = deque([start])
    visited = set()
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            return True
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                queue.append(neighbor)
    
    return False  # No path found

# DFS algorithm to find a path to the exit
def dfs_solver(maze, start, end):
    stack = [start]
    visited = set()
    
    while stack:
        current = stack.pop()
        
        if current == end:
            return True
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return False  # No path found

# Find the number of surrounding cells
def surrounding_cells(rand_wall):
    s_cells = 0
    if maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
        s_cells += 1
    return s_cells

BFST = []
DFST = []
SIZE = []

cpu = psutil.cpu_percent(interval=1,percpu=False)
memory = psutil.virtual_memory()

mem = memory.percent

for m in range(sizes):
    a = random.randint(0,1)
    # Initialize the maze
    maze = []
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append('u')
        maze.append(line)

    # Randomize the starting point and set it as a cell
    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1

    # Mark it as a cell and add surrounding walls to the list
    maze[starting_height][starting_width] = 'c'
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in the maze
    maze[starting_height - 1][starting_width] = 'w'
    maze[starting_height][starting_width - 1] = 'w'
    maze[starting_height][starting_width + 1] = 'w'
    maze[starting_height + 1][starting_width] = 'w'

    while walls:
        # Pick a random wall
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        # Check if it is a left wall
        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == 'c':
                s_cells = surrounding_cells(rand_wall)

                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if rand_wall[0] != 0:
            if maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == 'c':
                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if rand_wall[0] != height - 1:
            if maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == 'c':
                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1] - 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if [rand_wall[0], rand_wall[1] - 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Check the right wall
        if rand_wall[1] != width - 1:
            if maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == 'c':
                s_cells = surrounding_cells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[1] != width - 1:
                        if maze[rand_wall[0]][rand_wall[1] + 1] != 'c':
                            maze[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if [rand_wall[0], rand_wall[1] + 1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if rand_wall[0] != height - 1:
                        if maze[rand_wall[0] + 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0] - 1][rand_wall[1]] != 'c':
                            maze[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'u':
                maze[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, width):
        if maze[1][i] == 'c':
            maze[0][i] = 'c'
            break

    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == 'c':
            maze[height - 1][i] = 'c'
            break
    

    if a:
        if(sleep):
            time.sleep(0.5)

        # Measure time for DFS
        start_time = time.perf_counter()
        dfs_path = dfs_solver(maze, (0, 1), (height - 2, width - 2))
        dfs_time = time.perf_counter() - start_time
        

        if(sleep):
            time.sleep(0.5)
        # Measure time for BFS
        start_time = time.perf_counter()
        bfs_path = bfs_solver(maze, (0, 1), (height - 2, width - 2))
        bfs_time = time.perf_counter() - start_time

        if(log):
            print("MAZE:", m, " || SIZE:", height)
            print("DFS:")
            print("  Found:", dfs_path)
            print("  Time:", dfs_time)
            

            print("BFS:")
            print("  Found:", bfs_path)
            print("  Time:", bfs_time,"\n")

            
        
        if(bfs_path and dfs_path):
            DFST.append(dfs_time)
            BFST.append(bfs_time)
            height = height+increment
            width = height   
            SIZE.append(height)
    else:

        if(sleep):
            time.sleep(0.5)
        # Measure time for BFS
        start_time = time.perf_counter()
        bfs_path = bfs_solver(maze, (0, 1), (height - 2, width - 2))
        bfs_time = time.perf_counter() - start_time

        if(sleep):
            time.sleep(0.5)

        # Measure time for DFS
        start_time = time.perf_counter()
        dfs_path = dfs_solver(maze, (0, 1), (height - 2, width - 2))
        dfs_time = time.perf_counter() - start_time

        if(log):
            print("MAZE:", m, " || SIZE:", height)

            print("BFS:")
            print("  Found:", bfs_path)
            print("  Time:", bfs_time)

            print("DFS:")
            print("  Found:", dfs_path)
            print("  Time:", dfs_time,"\n")
            
        
        if(bfs_path and dfs_path):
            DFST.append(dfs_time)
            BFST.append(bfs_time)
            height = height+increment
            width = height    
            SIZE.append(height)

print("Date:",date,"\n")
time = time.perf_counter() - start
print("Time elapsed:", time, "\n")

print(f"MEM Usage before execution: {mem}%", "\n")
print(f"CPU Usage before execution: {cpu}%", "\n")
if printNum:
    

    print("BFS: ", end="")
    for b in BFST:
        print(b, " ", end="")
    
    print("\n")
    print("DFS: ", end="")
    for d in DFST:
        print(d, " ", end="")

    print("\n")
    print("SIZE: ", end="")
    for s in SIZE:
        print(s, " ", end="")

if plotit:
    plt.figure(figsize=(16, 12))
    plt.plot(SIZE, BFST, marker='o', label='BFS Time')
    plt.plot(SIZE, DFST, marker='o', label='DFS Time')
    plt.xlabel('Maze Size')
    plt.ylabel('Time (seconds)')
    plt.title('BFS and DFS Time vs. Maze Size')
    plt.grid(True)
    plt.legend()
    plt.show()