# mycopunk-hexfit

## Overview
The Hexagonal Grid Solver is a Python program designed to help users visualize and place hexagonal shapes within a specified hexagonal grid. The program allows users to define the dimensions of the grid and the shapes they wish to place, and it employs an algorithm to determine if the shapes can fit within the grid without overlapping.

## Features
- Define hexagonal grid dimensions (height and width).
- Specify various hexagonal shapes in a JSON format.
- Determine valid placements for the shapes within the grid.
- Visualize the grid and the placed shapes, generating output images for reference.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd hexagonal-grid-solver
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the main program:
   ```
   python src/main.py
   ```
2. Follow the prompts to enter the grid dimensions and specify the shapes.

## Example Shapes
Refer to the `examples/sample_shapes.json` file for a sample structure of how to define shapes.

## Testing
To run the tests, navigate to the `tests` directory and execute:
```
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.