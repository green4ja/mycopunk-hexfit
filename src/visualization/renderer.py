from matplotlib import pyplot as plt
import numpy as np
import os

def draw_hexagon(ax, center, size, color='blue'):
    """Draw a flat-topped hexagon on the given axes."""
    # Flat-topped hexagon angles (start at 0 for flat top)
    angles = np.linspace(0, 2*np.pi, 7)
    x_hex = center[0] + size * np.cos(angles)
    y_hex = center[1] + size * np.sin(angles)
    ax.fill(x_hex, y_hex, color=color, edgecolor='black', linewidth=0.5)
    return center

def hex_to_pixel(col, row, size=1.0):
    """Convert hex coordinates to pixel coordinates for flat-topped hexagons.
    This matches the Mycopunk game grid where columns 0,2,4 are higher.
    """
    # For flat-topped hexagons with even-r offset
    x = size * (3.0/2.0) * col
    # FIXED: Invert the offset so even columns (0,2,4) are higher
    y = size * np.sqrt(3) * (row + 0.5 * ((col + 1) % 2))
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
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Set the hexagon size
    hex_size = 0.5
    
    # Dictionary to store the pixel coordinates of each node in each shape
    shape_pixels = {}
    
    # Draw the empty hexagonal grid
    for row in range(grid.height):
        for col in range(grid.width):
            pixel = hex_to_pixel(col, row, hex_size)
            draw_hexagon(ax, pixel, hex_size, color='lightgrey')
    
    # Draw the shapes at their placed positions
    for shape, position in grid.placements:
        shape_pixels[shape.name] = {}
        
        # Choose color based on shape.color
        if hasattr(shape, 'color') and shape.color:
            if shape.color == "blue":
                color = "deepskyblue"
            elif shape.color == "purple":
                color = "violet"
            else:
                color = shape.color
        else:
            color = "gray"
            
        # Draw each node in the shape
        for node in shape.nodes:
            grid_pos = (position[0] + node[0], position[1] + node[1])
            pixel = hex_to_pixel(grid_pos[0], grid_pos[1], hex_size)
            center = draw_hexagon(ax, pixel, hex_size, color=color)
            shape_pixels[shape.name][(node[0], node[1])] = center

        # Draw connections between nodes
        if hasattr(shape, 'connections') and shape.connections:
            for conn in shape.connections:
                from_node = (conn['from']['x'], conn['from']['y'])
                to_node = (conn['to']['x'], conn['to']['y'])
                
                if from_node in shape_pixels[shape.name] and to_node in shape_pixels[shape.name]:
                    from_pixel = shape_pixels[shape.name][from_node]
                    to_pixel = shape_pixels[shape.name][to_node]
                    ax.plot([from_pixel[0], to_pixel[0]], [from_pixel[1], to_pixel[1]], 
                            color='black', linewidth=2, zorder=1)

    # Add shape names as text
    for shape, position in grid.placements:
        if shape.nodes:  # Make sure shape has nodes
            avg_x = sum(position[0] + node[0] for node in shape.nodes) / len(shape.nodes)
            avg_y = sum(position[1] + node[1] for node in shape.nodes) / len(shape.nodes)
            pixel = hex_to_pixel(avg_x, avg_y, hex_size)
            ax.text(pixel[0], pixel[1], shape.name, fontsize=8, ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.1'))

    # Set proper axis limits to show all hexagons
    ax.set_xlim(-1, (grid.width) * hex_size * 1.5 + 1)
    ax.set_ylim(-1, (grid.height + 1) * hex_size * np.sqrt(3) + 1)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
    
    plt.tight_layout()
    plt.show()

# Add an alias for backward compatibility
render_grid = visualize_grid