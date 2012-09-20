import pygame, random # a code test for myself. Stripped all functionality from main... < 60 lines 
limit = 72
max_cells = limit * limit
start_count = int( 0.16 * max_cells)
screen = pygame.display.set_mode([(limit-1 )* 5, (limit- 1)*5])
def spawn(count, limit):
    a_set = set()     
    x = rand(0, limit-1)
    y = rand(0, limit-1)
    for z in range(count):
        while ((x, y)) in a_set:
            x = rand(0, limit-1)
            y = rand(0, limit-1)
        a_set.add((x, y))
    return a_set
def create_potentials(passed_set):
    pot_set = set()
    for location in iter(passed_set):
        loc_x, loc_y = location
        for loop_x in range(-1,2):
            x = loop_x + loc_x
            if 0 > x or x > (limit-1): continue
            for loop_y in range(-1,2):
                y = loop_y + loc_y 
                if 0 > y or y > (limit-1): continue
                pot_set.add((x, y))
    return pot_set
def count_neighbors(cellA, passed_set):
    c = 0
    xA, yA = cellA
    for cellB in iter(passed_set):
        if cellA == cellB: continue
        xB, yB = cellB
        if abs(xB - xA) <= 1 and abs(yB - yA) <= 1:
            c += 1
    return c
def determine_next_gen(curr_list, pot_list):
    gen = set()
    for each_cell in iter(pot_list):
        neighbors = count_neighbors(each_cell, curr_list) 
        if neighbors == 3:
            gen.add(each_cell)
        if neighbors == 2 and each_cell in curr_list:
            gen.add(each_cell)
    return gen
def draw_cells_as_boxes():
    for each_cell in iter(cells):
        px, py = (each_cell[0]*5), (each_cell[1]*5)
        px_array[px:(px + 5), py:(py + 5)] = (175,95,175)
rand = random.randint
pygame.init()
cells = potentials = set()
cells = spawn(start_count, limit)
px_array = pygame.PixelArray(screen)
while True:
    pygame.display.flip()               #Draws the screen
    cells = determine_next_gen(cells, create_potentials(cells))
    screen.fill((0,0,0))
    draw_cells_as_boxes()