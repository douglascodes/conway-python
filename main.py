import pygame, random

class Environment():                       
    def __init__(self, measure=10): 
        self.limit = measure * measure
        self.max_cells = self.limit * self.limit
        self.vigor = 6.5/50.0
        self.start_count = int(self.vigor * self.max_cells)
        self.black = (0,0,0)
        self.cell_color = (175,95,175)
        self.screen = pygame.display.set_mode([(50 + ((self.limit-1 )* p_offset)), (50 + (self.limit- 1)*p_offset)])

class Dish():
    def __init__(self):
        self.create_time = pygame.time.get_ticks()
        self.cells = set()
        self.potentials = set()
        self.next_gen = set()
        self.prev_gen = set()
        
    def spawn(self, count, limit):
        if count > limit*limit:
            raise TooManyExpected()
            return
        a_set = set()     
        x = rand(0, limit-1)
        y = rand(0, limit-1)
        
        for z in range(count):
            while ((x, y)) in a_set:
                x = rand(0, limit-1)
                y = rand(0, limit-1)
            a_set.add((x, y))
        return a_set

    def take_turn(self):
        self.potentials = self.create_potentials(self.cells)
        self.prev_gen = self.cells 
        self.cells = self.determine_next_gen(self.cells, self.potentials)

    def create_potentials(self, passed_set):
        pot_set = set()
        for alpha in iter(passed_set):
            loc_x, loc_y = alpha

            for loop_x in range(-1,2):
                x = loop_x + loc_x
                if 0 > x or x > (env.limit-1): continue
                for loop_y in range(-1,2):
                    y = loop_y + loc_y 
                    if 0 > y or y > (env.limit-1): continue
                    pot_set.add((x, y))
        return pot_set

    def count_neighbors(self, cellA, passed_set):
        c = 0
        xA, yA = cellA
        for cellB in iter(passed_set):
            if cellA == cellB: continue
            xB, yB = cellB
            if abs(xB - xA) <= 1 and abs(yB - yA) <= 1:
                c += 1
        return c
    
    def determine_next_gen(self, curr_list, pot_list):
        x = set()
        for each_cell in iter(pot_list):
            neighbors = self.count_neighbors(each_cell, curr_list) 
            if neighbors == 3:
                x.add(each_cell)
            if each_cell in curr_list and neighbors == 2:
                x.add(each_cell)
        return x

def draw_pixels(p_list):
    for each_px in iter(p_list):
        px, py = each_px
        px_array[px][py] = color

def draw_cells_as_boxes(p_list, color):
    for each_cell in iter(p_list):
        px, py = each_cell[0]*p_offset, each_cell[1]*p_offset
        px_array[px:(px + p_offset), py:(py + p_offset)] = color

class TooManyExpected(Exception):
    def __init__(self):
        self.value = "Cell count exceeds limits."
    def __str__(self):
        return repr(self.value)

p_offset = 10
env = Environment(10)
clock = pygame.time.Clock()
rand = random.randint
thedish = Dish()
pygame.init()
color = env.cell_color
px_array = pygame.PixelArray(env.screen)
thedish.cells = thedish.spawn(env.start_count, env.limit)
draw_cells_as_boxes(thedish.cells, env.cell_color)
while True:
    pygame.display.flip()               #Draws the screen
    thedish.take_turn()
    env.screen.fill(env.black)
    draw_cells_as_boxes(thedish.cells, env.cell_color)
     