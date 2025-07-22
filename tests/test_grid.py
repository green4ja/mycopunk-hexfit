import unittest
from src.grid.hexgrid import HexGrid
from src.shapes.shape import Shape

class TestHexGrid(unittest.TestCase):

    def setUp(self):
        self.grid = HexGrid(width=6, height=5)

    def test_grid_creation(self):
        self.assertEqual(self.grid.width, 6)
        self.assertEqual(self.grid.height, 5)
        self.assertEqual(len(self.grid.cells), 30)  # Assuming 6 * 5 cells

    def test_add_shape(self):
        shape = Shape(nodes=[(0, 0), (1, 0), (0, 1)])  # Example shape
        self.grid.add_shape(shape, (0, 0))
        self.assertIn(shape, self.grid.shapes)

    def test_shape_placement_out_of_bounds(self):
        shape = Shape(nodes=[(0, 0), (1, 0), (0, 1)])
        result = self.grid.add_shape(shape, (10, 10))  # Out of bounds
        self.assertFalse(result)

    def test_shape_placement_valid(self):
        shape = Shape(nodes=[(0, 0), (1, 0), (0, 1)])
        result = self.grid.add_shape(shape, (1, 1))  # Valid placement
        self.assertTrue(result)

    def test_shape_overlap(self):
        shape1 = Shape(nodes=[(0, 0), (1, 0), (0, 1)])
        shape2 = Shape(nodes=[(0, 0), (1, 0), (0, 1)])
        self.grid.add_shape(shape1, (1, 1))
        result = self.grid.add_shape(shape2, (1, 1))  # Overlapping placement
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()