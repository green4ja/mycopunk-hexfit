import unittest
from src.grid.hexgrid import HexGrid
from src.shapes.shape import Shape
from src.solver.packing import PackingSolver

class TestPackingSolver(unittest.TestCase):

    def setUp(self):
        self.grid = HexGrid(5, 6)  # Create a hexagonal grid of 5 rows and 6 columns
        self.shapes = [
            Shape(name="Triangle", nodes=[(0, 0), (1, 0), (0, 1)]),  # Example shape
            Shape(name="Square", nodes=[(0, 0), (1, 0), (0, 1), (1, 1)])  # Another example shape
        ]
        self.solver = PackingSolver(self.grid, self.shapes)

    def test_solver_initialization(self):
        self.assertIsNotNone(self.solver)
        self.assertEqual(len(self.solver.shapes), 2)

    def test_find_valid_placement(self):
        result = self.solver.find_valid_placement()
        self.assertTrue(result)  # Expecting a valid placement to be found

    def test_no_valid_placement(self):
        # Modify the grid or shapes to ensure no valid placement is possible
        self.grid = HexGrid(1, 1)  # Too small for the shapes
        self.solver = PackingSolver(self.grid, self.shapes)
        result = self.solver.find_valid_placement()
        self.assertFalse(result)  # Expecting no valid placement to be found

if __name__ == '__main__':
    unittest.main()