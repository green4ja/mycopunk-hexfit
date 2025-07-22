class PackingSolver:
    def __init__(self, grid, shapes=None):
        self.grid = grid
        self.shapes = shapes if shapes is not None else []
        self.placements = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def can_place_shape(self, shape, position):
        # Check if the shape can be placed at the given position
        for node in shape.nodes:
            grid_position = (position[0] + node[0], position[1] + node[1])
            if not self.grid.is_within_bounds(grid_position) or not self.grid.is_empty(grid_position):
                return False
        return True

    def place_shape(self, shape, position):
        # Place the shape on the grid
        for node in shape.nodes:
            grid_position = (position[0] + node[0], position[1] + node[1])
            self.grid.place(grid_position, shape)
        # Record the placement
        self.placements.append((shape, position))
        self.grid.placements.append((shape, position))

    def remove_shape(self, shape, position):
        # Remove the shape from the grid
        for node in shape.nodes:
            grid_position = (position[0] + node[0], position[1] + node[1])
            self.grid.remove(grid_position)
        # Remove the placement
        if (shape, position) in self.placements:
            self.placements.remove((shape, position))
        if (shape, position) in self.grid.placements:
            self.grid.placements.remove((shape, position))

    def solve(self):
        if len(self.shapes) == 0:
            return True

        shape = self.shapes[0]
        remaining_shapes = self.shapes[1:]
        
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.can_place_shape(shape, (x, y)):
                    self.place_shape(shape, (x, y))
                    
                    # Recursive call with remaining shapes
                    old_shapes = self.shapes
                    self.shapes = remaining_shapes
                    if self.solve():
                        return True
                    self.shapes = old_shapes
                    
                    self.remove_shape(shape, (x, y))
        
        return False
    
    def find_valid_placement(self):
        # Bridge method to satisfy the tests
        return self.solve()

    def get_placements(self):
        return self.placements