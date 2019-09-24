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

# In progress - core functionality
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
* Get towers to do something useful
    - Give runner(s) stats: happiness (0 to 5), energy (0 to 10), hydration (0 to 10)
    - Let stats drop over time
    - (for now) when too low, runner disappears, print out the reason to the console
    - If a runner nearby, 'help' it
        - Supporter: increase happiness (up to 10)
        - Water stand: increase hydration (up to 10)
        - Food stand: increase food (up to 10)

# Improvements
* Improve route following and movement:
    - Smaller steps
    - Around the corner in a curve
    - Change runner image depending on the direction of travel
    - Animate runner - using multiple images
    - And make sure the current loop is completed before changing the orientation to avoid 'jitter'
* Spawn multiple runners
    - Initially at regular intervals
* Different types of runners
    - Use different images
* Show status of runners
    - low-energy icon (find one) when below threshold (put in settings, let's try 3)
    - low-water icon (find one) when below threshold (put in settings, let's try 3
    - unhappy, neutral, happy face - 1/2, 3, 4/5 (note: 0 means they leave, so no face required for this) 
* Improve tower-effects
    - Handle multiple runners
        - Work out which runners are next to which towers
        - Try to get each tower to serve a runner (could be an interesting algorithm)
 
 * To add:  The better a runner's stats are, the faster they'll go - so a nice way to see who's getting low. That could give a player two different aims: trying to achieve the faster time and/or to get as many runners over the finish line as possible
 