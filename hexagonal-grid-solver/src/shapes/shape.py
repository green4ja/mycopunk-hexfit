class Shape:
    def __init__(self, name, nodes, connections=None, color=None):
        self.name = name
        self.nodes = nodes  # List of tuples representing the coordinates of the nodes
        self.connections = connections if connections is not None else []  # Store connections between nodes
        self.color = color  # Add this line

    def get_layout(self):
        return self.nodes

    def get_connections(self):
        return self.connections

    def get_boundaries(self):
        min_x = min(node[0] for node in self.nodes)
        max_x = max(node[0] for node in self.nodes)
        min_y = min(node[1] for node in self.nodes)
        max_y = max(node[1] for node in self.nodes)
        return (min_x, max_x, min_y, max_y)
    
    def get_coordinates(self):
        # Return the coordinates of all nodes in this shape
        return self.nodes

    def __repr__(self):
        return f"Shape(name={self.name}, nodes={self.nodes})"