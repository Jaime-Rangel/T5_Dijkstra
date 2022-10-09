from cmath import sqrt
import enum
from importlib.resources import path
from turtle import Screen
from numpy import gradient, mat
import pygame as pg
from random import random
from collections import deque
from torch import greater
import bfs_helper as graph_helper
import obstacles as obs
from heapq import *
import dijkstra as djk
import math

size = 40
tile = 20
speed = 10

pg.init()

def get_circle(x,y):
    return (x * tile + tile // 2, y * tile + tile // 2),tile // 4

def get_rect(x,y):
    return x * tile + 1, y * tile + 1, tile - 2 , tile - 2

def rules_next_nodes(x,y,diagonal):
    #Limits of the array movements
    check_next_node = lambda x, y: True if 0 <= x < size and 0 <= y < size else False

    #How to move in the array the RULES!!!!
    if diagonal == False:
        ways = [-1, 0],[0, -1],[1, 0],[0, 1]
    else:
        ways = [-1, 0],[0, -1],[1, 0],[0, 1], [-1,1], [1,1], [-1,-1], [1,-1]

    listPesos = []

    for dx, dy in ways:
        # whe check the constraints sizes for array
        if check_next_node(x + dx, y + dy):
            if (dx == -1 and dy == 1) or (dx == 1 and dy == 1) or (dx == -1 and dy == -1) or (dx == 1 and dy ==-1):
                if(grid[y + dy][x + dx] != 9999999999):
                    listPesos.append([(math.sqrt(2)),(x + dx, y + dy)])
            else:
                listPesos.append([(grid[y + dy][x + dx]),(x + dx, y + dy)])

            #[(grid[y + dy][x + dx], (x + dx, y + dy))]
        # print(dx,dy)

    return listPesos
    # return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy) 
    # if (dx == -1 and dy == 1)]
    #return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

#Size of the working window
surface = pg.display.set_mode([size * tile,size * tile])
clock = pg.time.Clock()

# Data for calculate Dijkstra
start = (0, 0)
goal = (30,16) # N - 1 Sucker!!
allowDiagonals = True

grid = [['9999999999' if random() < 0.4 and (col != start[1] and row != start[0]) and
(col != goal[1] and row != goal[0]) else '1' for col in range(size)] for row in range(size)]

# grid = []

# for i in range(size):
#     values = ['1'] * size
#     grid.append(values)

grid = [[int(char) for char in string ] for string in grid]

#Graph
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        #Create a dictionary for paussible movements in the array
        what = rules_next_nodes(x, y, allowDiagonals)
        #what = graph.get((x, y), [])        
        graph[(x, y)] = rules_next_nodes(x, y, allowDiagonals)

print(graph)
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

while True:
    #Screen
    surface.fill(pg.Color('black'))

    #Obstacles
    obs.draw_obstacles(grid,get_rect,tile,surface,pg)

    # draw BFS work
    [pg.draw.rect(surface, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
    [pg.draw.rect(surface, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
    pg.draw.circle(surface,pg.Color('orange'), *get_circle(goal[1],goal[0]))

    # Dijkstra logic
    if queue:
        cur_cost, cur_node = heappop(queue)
        inv_goal = (goal[1],goal[0])

        if cur_node == inv_goal:
            queue = []
            print("Longitud:",cost_visited.get(inv_goal))
            #print(cost_visited)
            # for x in cost_visited:
            #     if(x[0] == x[])
            continue

        next_nodes = graph[cur_node]

        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node

            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                heappush(queue, (new_cost, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    # draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(surface, pg.Color('dodgerblue'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(surface, pg.Color('blue'), *get_circle(*start))
    pg.draw.circle(surface, pg.Color('yellow'), *get_circle(*path_head))

    #Display pygames window
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(speed)