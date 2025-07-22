class HexGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.shapes = []  # Keep track of all shapes placed on the grid
        self.placements = []  # Keep track of where shapes are placed (shape, position)

    def is_within_bounds(self, position):
        """Check if the position is within the grid boundaries."""
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def is_empty(self, position):
        """Check if the position is empty (no shape placed)."""
        x, y = position
        return self.grid[y][x] is None

    def place(self, position, shape):
        """Place a shape at the specified position."""
        x, y = position
        self.grid[y][x] = shape
        if shape not in self.shapes:
            self.shapes.append(shape)

    def remove(self, position):
        """Remove whatever is at the specified position."""
        x, y = position
        self.grid[y][x] = None

    def add_shape(self, shape, position):
        if self.can_place_shape(shape, position):
            for (dx, dy) in shape.get_coordinates():
                self.grid[position[1] + dy][position[0] + dx] = shape
            if shape not in self.shapes:
                self.shapes.append(shape)
            self.placements.append((shape, position))
            return True
        return False

    def can_place_shape(self, shape, position):
        for (dx, dy) in shape.get_coordinates():
            x, y = position[0] + dx, position[1] + dy
            if not self.is_within_bounds((x, y)) or not self.is_empty((x, y)):
                return False
        return True

    def __str__(self):
        grid_str = ""
        for row in self.grid:
            grid_str += " ".join(['.' if cell is None else 'X' for cell in row]) + "\n"
        return grid_str.strip()