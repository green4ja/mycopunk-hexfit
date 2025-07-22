from src.shapes.shape import Shape

def test_shape_initialization():
    shape = Shape(name="Triangle", nodes=[(0, 0), (1, 0), (0, 1)])
    assert shape.name == "Triangle"
    assert shape.nodes == [(0, 0), (1, 0), (0, 1)]

def test_shape_properties():
    shape = Shape(name="Triangle", nodes=[(0, 0), (1, 0), (0, 1)])
    assert shape.get_area() == 0.5  # Assuming a method to calculate area
    assert shape.get_perimeter() == 3.414  # Assuming a method to calculate perimeter

def test_shape_layout():
    shape = Shape(name="Triangle", nodes=[(0, 0), (1, 0), (0, 1)])
    layout = shape.get_layout()  # Assuming a method to get layout
    expected_layout = [(0, 0), (1, 0), (0, 1)]
    assert layout == expected_layout

def test_shape_boundaries():
    shape = Shape(name="Triangle", nodes=[(0, 0), (1, 0), (0, 1)])
    boundaries = shape.get_boundaries()  # Assuming a method to get boundaries
    expected_boundaries = [(0, 0), (1, 0), (0, 1), (0, 0)]
    assert boundaries == expected_boundaries