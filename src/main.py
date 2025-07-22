# main.py

import json
import os
import time
from src.grid.hexgrid import HexGrid
from src.shapes.shape import Shape
from src.solver.packing import PackingSolver
from src.visualization.renderer import render_grid

def get_user_input():
    height = int(input("Enter the height of the hexagonal grid: "))
    width = int(input("Enter the width of the hexagonal grid: "))
    
    # Ask for file path or direct JSON input
    input_choice = input("Enter 'f' to load from a file, or 'i' to input JSON directly: ").lower()
    
    if input_choice == 'f':
        file_path = input("Enter the path to the JSON file: ")
        with open(file_path, 'r') as file:
            shapes_data = json.load(file)
    else:
        shapes_input = input("Enter the shapes in JSON format: ")
        shapes_data = json.loads(shapes_input)
    
    return height, width, shapes_data

def main():
    try:
        height, width, shapes_data = get_user_input()
        
        grid = HexGrid(width, height)
        
        # Process shapes from JSON
        shapes = []
        for shape_data in shapes_data.get('shapes', []):
            # Extract nodes
            nodes = [(node['x'], node['y']) for node in shape_data['nodes']]
            
            # Extract connections
            connections = shape_data.get('connections', [])
            color = shape_data.get('color', None)
            
            # Create shape with nodes and connections
            shape = Shape(name=shape_data['name'], nodes=nodes, connections=connections, color=color)
            shapes.append(shape)
        
        solver = PackingSolver(grid, shapes)
        
        print(f"Attempting to fit {len(shapes)} shapes in a {width}x{height} grid...")
        start_time = time.time()
        
        if solver.solve():
            end_time = time.time()
            print(f"Solution found in {end_time - start_time:.2f} seconds!")
            
            # Generate output directory if it doesn't exist
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamp for unique filename
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(output_dir, f"solution_{timestamp}.png")
            
            # Visualize and save
            render_grid(grid, solver.get_placements(), save_path=output_file)
            print(f"Solution image saved to: {output_file}")
        else:
            end_time = time.time()
            print(f"No solution found after {end_time - start_time:.2f} seconds.")
            print("No valid combinations are possible.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()