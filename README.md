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
* Find images (isometric) of 'towers': bystanders, marshalls, etc
    - e.g. from https://kenney.nl/assets
* Drag and drop towers
    - Note: allow for multiple types of towers
    - Click on tower, start dragging
    - Show new position of the tower
    - When centre of tower base (roughly calculated/hand coded) is above a tile, highlight the tile (e.g. by drawing a rotated square around it)
    - When releasing tower, place on current tile
    - Drawing code to show placed towers
* Get towers to do something useful
    - If a runner nearby, 'help' it
        - Supporter: increase happiness (up to 10)
        - Water stand: increase hydration (up to 10)
        - Food stand: increase food (up to 10)

# Improvements
* Improve tower-effects
    - Handle multiple runners
        - Work out which runners are next to which towers
        - Try to get each tower to serve a runner (could be an interesting algorithm)
 
