import enum
from numpy import gradient
import pygame as pg
from random import random
from collections import deque
import bfs_helper as graph_helper

size = 20
tile = 20

pg.init()

def get_rect(x,y):
    return x * tile + 1, y * tile + 1, tile - 2 , tile - 2

def get_next_nodes(x,y):
    #Limits of the array movements
    check_next_node = lambda x, y: True if 0 <= x < size and 0 <= y < size and not grid[y][x] else False
   
    #How to move in the array
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]

    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

#Size of the working window
sc = pg.display.set_mode([size * tile,size * tile])
clock = pg.time.Clock()

# 0 and 1 matrix grid
grid = [[1 if random() < 0.2 else 0 for col in range(size)] for row in range(size)]

#Graph
graph = {}

for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# Settings
start = (0, 0)
queue = deque([start])
visited = {start:None}
cur_node = start


while True:
    #Screen
    sc.fill(pg.Color('black'))

    #draw grid with obstackles
    for y,row in enumerate(grid):
        for x, col in enumerate(row):
            # there's a 1 obstacle
            if col:
                #draw the obstacle
                pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=tile // 5)

    #bfs section
    for x,y in visited:
        pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y))
    
    for x,y in queue:
        pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y))
    
    if queue:
        #call bfs function for explore all paths
        visited = graph_helper.bfs(queue,visited,graph)
    
    path_head, path_segment = cur_node,cur_node

    #Display pygames window
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(50)