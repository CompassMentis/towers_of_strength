# towers_of_strength
Towers of Strength game for PyWeek 28

# Getting started
* Clone the repo
* (optional) Create a virtual environment, with Python 3.7
    * I usually name it '.env', which is already excluded with .gitignore, but feel free to use your own system. Just remember to update .gitignore if necessary
* Activate the virtual environment
* pip install - requirements.txt
* python main.py
* Currently the close button doesn't work. Instead use ^C

# Progress
* Level loaded from csv file
* Tiles shown

# In progress
* Calculate route from tiles, assume simple scenario:
    - Path doesn't cross
    - Start with 'SPN' (spawn) tile
    - Find neighbour which is not 'T' and not already found and add to list
    - Repeat with neighbour
    - return the list
* From route, calculate a path, starting simple
    - A straight line through the centre
    - Or two half-length straight lines meeting in the centre for corner pieces
* Move an image (e.g. a runner) along the route, start to finish
* Sketch an interface, with the following components:
    - Tiles (as currently generated)
    - A few 'towers' to place (e.g. a bystander and a marshall)
* Find images (isometric) of 'towers': bystanders, marshalls, etc
    - e.g. from https://kenney.nl/assets
* Show towers on the screen (not on the tiles, just ready to be dragged)
* Drag and drop towers
    - Note: allow for multiple types of towers
    - Click on tower, start dragging
    - Show new position of the tower
    - When centre of tower base (roughly calculated/hand coded) is above a tile, highlight the tile (e.g. by drawing a rotated square around it)
    - When releasing tower, place on current tile
    - Drawing code to show placed towers
