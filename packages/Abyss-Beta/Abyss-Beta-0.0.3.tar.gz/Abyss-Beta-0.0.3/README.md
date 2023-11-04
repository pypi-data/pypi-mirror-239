# Nebula Engine

## Overview:
### - Nebula Engine is a game engine built using Python, Pygame, and PyOpenGL. It aims to provide a user-friendly interface for game development, complete with a level editor and customizable terminal. The engine is designed to be modular and extensible, offering a range of features from asset management to custom rendering.

## Features
### Clock: Manages game time and frame rate.
### Display: Handles the game window and rendering.
### Canvas: Provides a surface for drawing game elements.
### AssetManager: Manages game assets and caches them for quick access.
### Camera: Manages the camera's position, speed, and other properties.
### Physics: Handles physics for game entities.
### Entity: Represents a game entity with methods for updating physics and rendering.
### Renderer: Manages the rendering of game entities and assets.
### Tilemap: Manages the game's tilemap and includes methods for rendering and collision detection.

## Setup
### PyPi:
- Run the command: ```pip install Nebula-Beta```
- Create a python file in the root of your projcet dir: ```cd MyProject``` -> ```touch game.py```
- Create a .ncfg file in the root of your project dir: ```cd MyProject``` -> ```touch .ncfg```
- Inside your python file set up the necessary imports:
```
from Nebula.Nebula import Nebula
from Nebula import NebulaObject
from Nebula import NebulaCore
```
- When you run the file with Nebula imported, it will look for your /ncfg and configure your project for you!
### GitHub:
- Clone the repository: ```git clone https://github.com/setoyuma/NebulaEngine.git```
- Navigate to the project directory: ```cd NebulaEngine```
- Run the setup script: ```python Nebula/_setup.py```

## Usage
## Here's a simple example to get you started:
```python
from Nebula.Nebula import Nebula
from Nebula import NebulaObject
from Nebula import NebulaCore
class Game:
    def __init__(self):
        # Initialize Nebula Engine components
        self.clock = Nebula.Clock
        self.camera = Nebula.Camera
        # ... (rest of the initialization)

    def update(self):
        # Update game logic
        # ...

    def render(self):
        # Render game elements
        # ...

    def run(self):
        # Main game loop
        # ...

Game().run()
```
