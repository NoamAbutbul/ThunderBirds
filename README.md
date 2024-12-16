# ThunderBirds

## Name

The game ThunderBirds is about two space ships to escape from a maze by go into a portal.

## Description

The game is running via terminal at this moment, but there is a strong base to
build the output screen for other platforms.

## Installation

To install and run the game, follow the instructions below:

- Clone the repository
- Navigate to the project directory
- Install the required dependencies

### Clone The Repository

Use the following command to clone the repository:

```bash
git clone https://github.com/NoamAbutbul/ThunderBirds.git
```

### Navigate To The Project Directory

after cloning the repository, navigate into the project directory:

```bash
cd thunderbirds
```

### Install The Required Dependencies

You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Follow the instructions below to play the game:

### Run The Game

You can run the game using the following command:

```bash
python main.py
```

TODO -> write here the python version the client need, and recommend him to open a venv

## Rules

The game starts with three lives per level.
Each mistake in the game will result in the level restarting and one life being deducted.
Each level has a certain time limit to complete the level.
If the level is not completed within this time, it is considered a foul.

Game Objects:

- Big Ship
- Small Ship
- Block Numbers
- Block Letters
- Wall
- Portal

The goal is to reach the portal with both ships. The walls in the game cannot be moved.
The ships can push blocks if their mass is greater than the block's mass.
The big ship can push block letters, and the small ship can push block numbers.

The mass of the block is determined by the number of pixels in the object.
The big ship has 10 mass, and the small ship has 5 mass.

If a block falls onto a ship and its mass is greater, it is considered a foul.
However, if the block's mass is smaller than the current power of the ship, the block will move in the direction of the ship.

If the external walls of the game have a hole on both sides of the board game limit,
it will be an option to move from one side of the wall to the other.

## How To Play

Follow the instruction in the start menu in the game to start a new game.

### Controls

The game can be controlled using the following keys:

- a: Move left
- d: Move right
- w: Move up
- s: Move down
- g: Switch ship

The current ship will be moving in the button direction (if legally)
until another direction will be pressed, or switch ship button will be pressed.

## Changing Settings Configuration

You can change the game settings configuration by change the 'consts.yaml' file.
There is an option to change the board limit by adjust the ROWS and COLS values,
in addition there is an option to change the game objects colors and game information colors.

### The Available Colors:

red, green, yellow, blue, magenta, cyan, white, grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, black.
