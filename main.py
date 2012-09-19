import pygame, random, sys, os
from pygame.locals import *

def exit_game(): 
    pygame.quit()
    os._exit(0)
 
def check_key():
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: return True
    return False

class Environment():                       
    def __init__(self, measure=10): 
        self.unit = measure                     
        self.limit = measure * measure
        self.max_cells = self.limit * self.limit
        self.vigor = 5.0/50.0
        self.start_count = int(self.vigor * self.max_cells)
        self.black = (0,0,0)
        self.cell_color = (255,255,255)
        self.screen = pygame.display.set_mode([self.limit,self.limit])
        self.looptime = 30              

class Dish():
    def __init__(self):
        self.create_time = pygame.time.get_ticks()
        self.cells = set()
        self.potentials = set()
        self.next_gen = set()
        self.cell_count = len(self.cells)
        
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

    def create_potentials(self, passed_set):
        pot_set = set()
        for alpha in iter(passed_set):
            loc_x, loc_y = alpha
            for x in range(-1,2):
                for y in range(-1,2):
                    pot_set.add((loc_x + x, loc_y + y))
                    
        pot_set = pot_set.union(passed_set)
        return pot_set

## fix this loop       
    def count_neighbors(self, cellA, passed_set):
        c = 0
        xA, yA = cellA
        for cellB in iter(passed_set):
            if cellA == cellB: continue
            xB, yB = cellB
            if abs(xB - xA) <= 1 and abs(yB - yA) <= 1:
                c += 1
        return c
    
    def determine_next_gen(self):
        self.potentials.clear()
        self.potentials = self.create_potentials(self.cells)
        self.next_gen.clear()
        for each_cell in iter(self.potentials):
            neighbors = self.count_neighbors(each_cell, self.potentials)
            self.next_gen.add(each_cell)
        self.cells = self.next_gen
        return

def draw_pixels(p_list):
    for each_px in iter(p_list):
        px, py = each_px
        px_array[px][py] = color

      
class TooManyExpected(Exception):
    def __init__(self):
        self.value = "Cell count exceeds limits."
    def __str__(self):
        return repr(self.value)

env = Environment(8)
clock = pygame.time.Clock()
rand = random.randint
thedish = Dish()
pygame.init()

color = env.cell_color
px_array = pygame.PixelArray(env.screen)
thedish.cells = thedish.spawn(env.start_count, env.limit)
draw_pixels(thedish.cells)
pygame.display.flip()           #Draws the screen

env.screen.fill(env.black)           #fills the background with named color
thedish.determine_next_gen()
draw_pixels(thedish.cells)


#while not check_key():
#    thedish.determine_next_gen()
        