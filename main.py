from typing import List, Tuple, Set
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

# Type aliases
Shape = List[Tuple[int, int]]
GridPos = Tuple[int, int]

# === Shape Utilities ===

def place_shape(shape: Shape, anchor: GridPos) -> List[GridPos]:
    aq, ar = anchor
    placed = []
    for dq, dr in shape:
        # Odd-q vertical layout: odd columns are shifted down
        shift = 1 if (aq % 2 == 1 and dq % 2 != 0) else 0
        placed.append((aq + dq, ar + dr + shift))
    return placed

def fits_in_grid(placed_shape: List[GridPos], width: int, height: int) -> bool:
    return all(0 <= q < width and 0 <= r < height for (q, r) in placed_shape)

def overlaps(placed_shape: List[GridPos], occupied: Set[GridPos]) -> bool:
    return any(cell in occupied for cell in placed_shape)

def are_adjacent(a: GridPos, b: GridPos) -> bool:
    # 4-way adjacency (horizontal/vertical)
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def get_hex_neighbors(pos: GridPos) -> List[GridPos]:
    q, r = pos
    if q % 2 == 0:  # even-q
        offsets = [(+1,  0), (+1, -1), (0, -1),
                   (-1, -1), (-1,  0), (0, +1)]
    else:  # odd-q
        offsets = [(+1, +1), (+1,  0), (0, -1),
                   (-1,  0), (-1, +1), (0, +1)]
    return [(q + dq, r + dr) for dq, dr in offsets]

def are_adjacent_hex(a: GridPos, b: GridPos) -> bool:
    return b in get_hex_neighbors(a)

def preserves_adjacency(shape: Shape, placed_shape: List[GridPos]) -> bool:
    n = len(shape)
    for i in range(n):
        orig_adj = set(j for j in range(n) if i != j and are_adjacent_hex(shape[i], shape[j]))
        placed_adj = set(j for j in range(n) if i != j and are_adjacent_hex(placed_shape[i], placed_shape[j]))
        if orig_adj != placed_adj:
            print("Adjacency mismatch detected:")
            for k in range(n):
                print(f"  Part {k}: original {shape[k]} → placed {placed_shape[k]}")
            print(f"  At part {i}, expected adjacency: {orig_adj}, got: {placed_adj}")
            return False
    return True

# === Solver ===

def solve(shapes: List[Shape], width: int, height: int) -> List[Tuple[GridPos, List[GridPos]]]:
    solution = []

    def backtrack(index: int, occupied: Set[GridPos]) -> bool:
        nonlocal solution
        if index == len(shapes):
            return True
        shape = shapes[index]
        for q in range(width):
            for r in range(height):
                placed = place_shape(shape, (q, r))
                if not fits_in_grid(placed, width, height):
                    continue
                if overlaps(placed, occupied):
                    continue
                if not preserves_adjacency(shape, placed):
                    continue
                solution.append(((q, r), placed))
                for cell in placed:
                    occupied.add(cell)
                if backtrack(index + 1, occupied):
                    return True
                for cell in placed:
                    occupied.remove(cell)
                solution.pop()
        return False

    if backtrack(0, set()):
        return solution
    else:
        return []

# === Drawing Utilities ===

def draw_hex_grid_with_shapes(width, height, solution):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import random
    import math

    size = 1
    dx = size * 3/2
    dy = size * math.sqrt(3)

    fig_width = width * dx * 0.7
    fig_height = height * dy * 0.7
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw grid (odd-q vertical layout, (0,0) top-left)
    for q in range(width):
        for r in range(height):
            x = dx * q
            y = dy * r + (dy / 2 if q % 2 == 1 else 0)
            hexagon = patches.RegularPolygon((x, y), numVertices=6, radius=size * 0.95, orientation=math.radians(30), edgecolor='brown', facecolor='none', linewidth=2)
            ax.add_patch(hexagon)

    # Assign random colors to shapes
    colors = []
    for _ in solution:
        colors.append([random.random() for _ in range(3)])

    # Draw shapes
    for idx, (_, cells) in enumerate(solution):
        color = colors[idx]
        for (q, r) in cells:
            x = dx * q
            y = dy * r + (dy / 2 if q % 2 == 1 else 0)
            hexagon = patches.RegularPolygon((x, y), numVertices=6, radius=size * 0.85, orientation=math.radians(30), edgecolor='black', facecolor=color, linewidth=2)
            ax.add_patch(hexagon)

    # Set axis limits to fit grid
    ax.set_xlim(-size, dx * width + size)
    ax.set_ylim(-size, dy * height + size)
    ax.invert_yaxis()  # <-- Flip the image vertically

    plt.tight_layout()
    plt.show()

# === Example Usage ===

if __name__ == "__main__":
    # Green 4 up to right
    shape1 = [
        (0, 0),
        (0, 1),
        (1, 0),
        (2, 0)
    ]

    # Green f without middle 3
    shape2 = [
        (0, 0),
        (-1, 0),
        (-1, 1),
    ]

    # Blue T 5
    shape3 = [
        (0, 0),
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, 2)
    ]

    # Straight Up 3
    shape4 = [
        (0, 0),
        (0, 1),
        (0, 2)
    ]
    
    # Blue W 5
    shape5 = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0)
    ]

    # Purple f without middle 5
    shape6 = [
        (0, 0),
        (-1, 0),
        (-1, 1),
        (-1, 2),
        (-1, 3)
    ]

    # #9 Legendary Large
    # shape1 = [
    #     (-2, 1),
    #     (-1, 0),
    #     (0, 0),
    #     (1, 0),
    #     (0, 1),
    #     (1, 1),
    #     (0, 2),
    #     (-1, 2),
    #     (0, 3)
    # ]

    # # 3 tall offshoot
    # shape2 = [
    #     (0, 0),
    #     (0, 1),
    #     (1, 1),
    #     (0, 2)
    # ]

    # # 4 Blue squiggle
    # shape3 = [
    #     (-2, 1),
    #     (-1, 0),
    #     (0, 0),
    #     (-1, 1)
    # ]

    # # Blue traingle 3
    # shape4 = [
    #     (0, 0),
    #     (1, 0),
    #     (0, 1)
    # ]

    # # Green 3 long
    # shape5 = [
    #     (0, 0),
    #     (1, 0),
    #     (2, 0)
    # ]

    # # Green backwards L 3
    # shape6 = [
    #     (0, 0),
    #     (0, 1),
    #     (-1, 1)
    # ]


    shapes = [shape1, shape2, shape3, shape4, shape5, shape6]
    width, height = 6, 5

    solution = solve(shapes, width, height)

    if solution:
        print("Found solution:")
        for (anchor, cells) in solution:
            print(f"Shape at anchor {anchor}: {cells}")
        draw_hex_grid_with_shapes(width, height, solution)
    else:
        print("No solution found.")
