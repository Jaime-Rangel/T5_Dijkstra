def draw_obstacles(grid,get_rect,tile,surface,pg):
    #draw grid with obstackles
    for y,row in enumerate(grid):
        for x, col in enumerate(row):
            # there's a 1 obstacle
            if col:
                #draw the obstacle
                pg.draw.rect(surface, pg.Color('darkorange'), get_rect(x, y), border_radius=tile // 5)
    return pg
