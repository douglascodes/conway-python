import unittest
from main import Dish
from main import Environment
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
        self.test_set.add((0,0))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(9, len(self.test_set), "Set should have 9 elements.")
    
    def test_neighbor_count_eight(self):
        self.test_set = set()
        self.test_set.add((0,0))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(8, self.d.count_neighbors( (0,0), self.test_set), "Neighbors should be 8")

    def test_neighbor_count_three(self):
        self.test_set = set()
        self.test_set.add((0,0))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(3, self.d.count_neighbors( (0,-2), self.test_set), "Neighbors should be 3")

    def test_neighbor_count_five(self):
        self.test_set = set()
        self.test_set.add((0,0))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(5, self.d.count_neighbors( (-1, 0), self.test_set), "Neighbors should be 5")

    def test_neighbor_count_one(self):
        self.test_set = set()
        self.test_set.add((0,0))
        self.test_set = self.d.create_potentials( self.test_set )
        self.assertEqual(1, self.d.count_neighbors( (-2, -2), self.test_set), "Neighbors should be 1")

    def test_generation_next(self):
        self.d.cells = self.d.spawn(100, 20)
        x = self.d.determine_next_gen()
        y = self.d.determine_next_gen()
        self.assertTrue(self.d.potentials >= self.d.cells, "Not a subset.")
        self.assertTrue(self.d.potentials >= self.d.next_gen, "Not a subset.")
        self.assertTrue(x == y, "Should give same result with repeated runs.")

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.e = Environment()
       
    def tearDown(self):
        self.e = None
        
    def test_env_creation(self):
        self.assertGreater(self.e.start_count, 0, "Env start count is <= 0")
        
    def test_color_difference(self):
        self.assertNotEqual(self.e.cell_color, self.e.black, "Cells and background should not be same color.")

def test_main():
    test_support.run_unittest(TestWorld,
                              TestEnvironment
                             )

if __name__ == '__main__':
    test_main()