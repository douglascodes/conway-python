import unittest
from main import Dish
from main import Environment
import pygame
import main
from test import test_support

class TestWorld(unittest.TestCase):

    def setUp(self):
        self.d = Dish()
        self.c = self.d.cells
        self.p = self.d.potentials

    def tearDown(self):
        self.d = None
        self.c = None
        self.p = None

    def test_dish_creation(self):
        self.assertIsInstance(self.d, Dish, "Is not a Dish instance")
    
    def test_dish_cells_empty(self):
        self.assert_(not self.d.cells, "Is not an empty set.")

    def test_dish_cells_addition(self):
        self.d.cells.add("s")
        self.assert_(self.d.cells, "Is an empty set.")
        
    def test_no_duplication(self):
        self.d.cells.add("s")
        self.d.cells.add("r")
        self.c_len = len(self.d.cells)
        self.d.cells.add("s")
        self.assertEqual(self.c_len, len(self.d.cells), "Error in length check.")

    def test_cells_removal(self):
        self.c.add("a")
        self.c_len = len(self.c)
        self.c.remove("a")
        self.assertNotEqual(self.c_len, len(self.c), "Error in length check.")
    
    def test_create_dish(self):
        self.limit = 100
        self.desired = self.limit * self.limit
        self.spawn_list = self.d.spawn(self.desired, self.limit)
        self.spawn_count = len(self.spawn_list)
        self.assertEqual(self.spawn_count, self.desired, "Did not return same created # as sent.")   
        
    def test_dish_spawn_limit(self):
        self.limit = 100
        self.desired = self.limit * self.limit
        self.assertRaises(main.TooManyExpected, self.d.spawn, self.desired+1, self.limit)

    def test_gets_all_nine_possible(self):
        self.test_set = set()
        self.test_set.add((5,5))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(9, len(self.test_set), "Set should have 9 elements.")
    
    def test_neighbor_count_eight(self):
        self.test_set = set()
        self.test_set.add((5,5))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(8, self.d.count_neighbors( (5,5), self.test_set), "Neighbors should be 8")

    def test_neighbor_count_three(self):
        self.test_set = set()
        self.test_set.add((5,5))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(3, self.d.count_neighbors( (5,3), self.test_set), "Neighbors should be 3")

    def test_neighbor_count_five(self):
        self.test_set = set()
        self.test_set.add((5,5))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(5, self.d.count_neighbors( (4, 5), self.test_set), "Neighbors should be 5")

    def test_neighbor_count_one(self):
        self.test_set = set()
        self.test_set.add((5,5))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(1, self.d.count_neighbors( (3, 3), self.test_set), "Neighbors should be 1")

    def test_expected_gen(self):
        self.test_set = set()
        self.result_expected = set()
        self.result_expected.add((6,6))
        self.result_expected.add((5,6))
        self.result_expected.add((4,6))
        self.test_set.add((5,5))
        self.test_set.add((5,6))
        self.test_set.add((5,7))
        self.assertNotEqual(self.test_set, self.result_expected, "Sets should not equal to start.")
        self.pot_set = self.d.create_potentials(self.test_set)
        self.result_set = self.d.determine_next_gen(self.test_set, self.pot_set)
        self.assertEqual(self.result_set, self.result_expected, "Sets should be same at end.")
        

    def test_generation_next(self):
        self.d.cells = self.d.spawn(100, 20)
        self.d.potentials = self.d.create_potentials(self.d.cells)
        self.next_gen = self.d.determine_next_gen(self.d.cells, self.d.potentials)
        self.assertTrue(self.d.potentials >= self.d.cells, "Not a subset.")
        self.assertTrue(self.d.potentials >= self.d.next_gen, "Should give same result with repeated runs.")

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.e = Environment()
       
    def tearDown(self):
        self.e = None
        
    def test_env_creation(self):
        self.assertGreater(self.e.start_count, 0, "Env start count is <= 0")
        
    def test_color_difference(self):
        self.assertNotEqual(self.e.cell_color, self.e.black, "Cells and background should not be same color.")

class TestDrawingMachine(unittest.TestCase):
    def setUp(self):
        self.env = Environment(10)
        self.color = main.env.cell_color
        self.px_array = main.px_array
        self.p_test = set()
        self.color = self.env.cell_color
        self.d = main.thedish
        
    def tearDown(self):
        self.env = None

    def test_pxarray_assignment(self):
        self.px_array[5][5] = self.color
        c = self.px_array[5][5]
        self.assertEqual(c, main.env.screen.map_rgb(self.color), "Pixel doesn't match")

    def test_drawing_all_cells(self):
        main.env.screen.fill(main.env.black) 
        main.draw_pixels(self.d.cells)
        pygame.display.flip()
        for each_cell in iter(self.d.cells):
            xC, yC = each_cell
            c = main.px_array[xC][yC]
            self.assertEqual(c, main.env.screen.map_rgb(self.color), "Pixels don't match")

    def test_draw_box(self):
        pass

def test_main():
    test_support.run_unittest(TestWorld,
                              TestEnvironment,
                              TestDrawingMachine
                             )

if __name__ == '__main__':
    test_main()