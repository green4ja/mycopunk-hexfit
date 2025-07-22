from matplotlib import pyplot as plt
import numpy as np
import os

def draw_hexagon(ax, center, size, color='blue'):
    """Draw a hexagon on the given axes."""
    angles = np.linspace(0, 2 * np.pi, 7)
    x_hex = center[0] + size * np.cos(angles)
    y_hex = center[1] + size * np.sin(angles)
    ax.fill(x_hex, y_hex, color=color, edgecolor='black')
    return (center[0], center[1])  # Return center for connection lines

def hex_to_pixel(col, row, size=1.0):
    """Convert hex coordinates to pixel coordinates for pointy-topped, even-q vertical layout (columns 0,2,4 are higher)."""
    x = size * np.sqrt(3) * col
    y = size * (1.5 * row + 0.75 * (col % 2))
    return (x, y)

def get_shape_color(shape):
    # Use the color property if present, otherwise fallback
    if hasattr(shape, 'color') and shape.color:
        if shape.color == "blue":
            return "deepskyblue"
        if shape.color == "purple":
            return "violet"
        if shape.color == "green":
            return "limegreen"
        if shape.color == "orange":
            return "orange"
    return "gray"  # fallback

def visualize_grid(grid, shapes, save_path=None):
    """Visualize the hexagonal grid and the placed shapes."""
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw the empty hexagonal grid
    for row in range(grid.height):
        for col in range(grid.width):
            pixel = hex_to_pixel(col, row)
            draw_hexagon(ax, pixel, 1, color='lightgrey')

    # --- FIX: Add this dictionary to store node pixel positions ---
    shape_pixels = {}

    # Draw the shapes at their placed positions and record node positions
    for shape, position in grid.placements:
        shape_pixels[shape.name] = {}
        for node in shape.nodes:
            grid_pos = (position[0] + node[0], position[1] + node[1])
            pixel = hex_to_pixel(grid_pos[0], grid_pos[1])
            color = get_shape_color(shape)
            center = draw_hexagon(ax, pixel, 1, color=color)
            shape_pixels[shape.name][(node[0], node[1])] = center

    # Draw connections between nodes
    for shape, position in grid.placements:
        if hasattr(shape, 'connections') and shape.connections:
            for conn in shape.connections:
                from_node = (conn['from']['x'], conn['from']['y'])
                to_node = (conn['to']['x'], conn['to']['y'])
                if from_node in shape_pixels[shape.name] and to_node in shape_pixels[shape.name]:
                    from_pixel = shape_pixels[shape.name][from_node]
                    to_pixel = shape_pixels[shape.name][to_node]
                    ax.plot([from_pixel[0], to_pixel[0]], [from_pixel[1], to_pixel[1]], 
                            color='black', linewidth=2.5, zorder=1)

    # Add shape names as text
    for shape, position in grid.placements:
        avg_x = sum(position[0] + node[0] for node in shape.nodes) / len(shape.nodes)
        avg_y = sum(position[1] + node[1] for node in shape.nodes) / len(shape.nodes)
        pixel = hex_to_pixel(avg_x, avg_y)
        ax.text(pixel[0], pixel[1], shape.name, fontsize=12, ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
    
    plt.tight_layout()
    plt.show()

# Add an alias for backward compatibility
render_grid = visualize_grid