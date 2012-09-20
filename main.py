import pygame, random
from pygame.locals import *

def check_key():
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.key == K_ESCAPE: return False
    return True


class Environment():                       
    def __init__(self, measure=8.5): 
        self.limit = int(measure * measure)
        self.max_cells = self.limit * self.limit
        self.vigor = 30.0/100.0       #Change this to increase start cell count
        self.start_count = int(self.vigor * self.max_cells)
        self.black = (0,0,0)
        self.cell_color = (175,95,175)
        self.border = 50
        self.screen = pygame.display.set_mode([(self.border*2 + ((self.limit-1 )* p_offset)), (self.border*2 + (self.limit- 1)*p_offset)])

class Dish():
    """Petry dish where all things happen. More commenting forthcoming.
    Check the main_test.py file for a better understanding of what is going on.
    http://en.wikipedia.org/wiki/Conway's_Game_of_Life
    ^ The rules.
    """

    def __init__(self):
        self.create_time = pygame.time.get_ticks()
        self.cells = set()
        self.potentials = set()
        self.next_gen = set()
        self.prev_gen = set()
        self.generation = 1
        self.cells = self.spawn(env.start_count, env.limit)
        self.pause = False

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
        if self.pause: return 
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
        gen = set()
        for each_cell in iter(pot_list):
            neighbors = self.count_neighbors(each_cell, curr_list) 
            if neighbors == 3:
                gen.add(each_cell)
            if each_cell in curr_list and neighbors == 2:
                gen.add(each_cell)
        return gen

def draw_pixels(p_list):
    for each_px in iter(p_list):
        px, py = each_px
        px_array[px][py] = color

def draw_cells_as_boxes(p_list, color):
    for each_cell in iter(p_list):
        px, py = env.border + (each_cell[0]*p_offset), env.border + (each_cell[1]*p_offset)
        px_array[px:(px + p_offset), py:(py + p_offset)] = color

class TooManyExpected(Exception):
    def __init__(self):
        self.value = "Cell count exceeds limits."
    def __str__(self):
        return repr(self.value)

p_offset = 5
env = Environment()
rand = random.randint
thedish = Dish()
pygame.init()
color = env.cell_color
pygame.display.set_caption("___ Conway's Game of Life ___ Douglas H. King ___  ESC to Exit ___")
px_array = pygame.PixelArray(env.screen)
draw_cells_as_boxes(thedish.cells, env.cell_color)

font = pygame.font.Font(None, 36)
    

while check_key():
    pygame.event.clear()
    pygame.display.flip()               #Draws the screen
    thedish.take_turn()
    thedish.generation += 1
    env.screen.fill(env.black)
    draw_cells_as_boxes(thedish.cells, env.cell_color)
    print thedish.generation 
    #uncomment to see a generation counter in console 