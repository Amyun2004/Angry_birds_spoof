# Angry Birds Game (Basic Replica)

## Overview
This project is a basic replica of the popular Angry Birds game, developed entirely in Python using the graphics.py module. 
No external libraries like Pygame or prebuilt physics engines were used. 
The game includes custom-built physics and an interactive graphical interface for user engagement.

## Directory Structure
Ensure all the following files are in the same directory:

1. graphics.py : Required for rendering the graphical elements. Download this module and place it in the same directory as the other files.
2. environment.py : Manages the game interface and interactions between the user and the game.
3. testing.py : Contains the custom-built physics engine that powers the game mechanics.

## How to Run the Game
1. Download and place graphics.py, environment.py, and testing.py in the same directory.
2. Open the environment.py file in your preferred code editor or Python IDLE.
3. Run the environment.py file to start the game.

## Gameplay Instructions
- The goal is to score above **50,000 points** within **five chances**.
- Points are awarded based on interactions:
  - Ball-to-ball interaction: 10 points.
  - Block-to-ball interaction: 5 points.
- The **red ball** (the one launched by the user) will reappear and become launchable again after it completely stops moving.

## Features
- Custom physics engine built from scratch using graphics.py.
- Interactive graphical interface for launching the red ball and observing the physics interactions.
- Point system to keep track of player progress.

## Requirements
- Python 3.x
- graphics.py module (ensure it is in the same directory as the other files).

## Notes
- Ensure no external libraries or physics engines are installed, as this project is designed to work exclusively with the graphics.py module and the custom physics engine in testing.py.
- If you encounter any issues, ensure all files are in the correct directory and check for Python version compatibility.

Enjoy playing the game!

