# Flappy Bird AI

## Project Setup

Download a text editor, such as Sublime Text.

[Link to Download Sublime Text](https://www.sublimetext.com/)

In a VSCode Command Prompt, setup the local project directory:

```sh
mkdir flappy_bird_ai
cd flappy_bird_ai
```

Head to github.com and create a new repository named `flappy_bird_ai`.

After completing that, create a new repository on the command line:

```sh
echo "# flappy_bird_ai" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/MylesThomas/flappy_bird_ai.git
git push -u origin main
```

Save this file as a markdown file `flappy_bird_ai/instructions.md`, then open up a new VSCode instance and Open folder > `flappy_bird_ai`.

Setup a virtual Python environment:

```sh
cd flappy_bird_ai
py -m venv env
```

You should now see a folder 'env' with a python.exe program in the /Scripts directory.

Create a .gitignore file for the Python project and save it in the root directory `flappy_bird_ai`:

```sh
cd flappy_bird_ai
echo > .gitignore
```

Code for .gitignore: [Link to file](https://github.com/github/gitignore/blob/main/Python.gitignore)

Activate the virtual environment in the terminal:

```sh
where python
.\env\Scripts\activate

python.exe -m pip install --upgrade pip
pip list
```

Note: You can leave the virtual environment with this call:

```sh
deactivate
```

Install the necessary packages into your virtual environment:

```sh
pip install pygame neat-python
```

Note: neat is a different module, so even though it looks odd that we are downloading neat-python and later will call import neat, this is correct.

Create a requirements.txt file to ensure that you have the necessary dependencies to run this code:

```sh
python -m pip freeze > requirements.txt # create a requirements.txt file
python -m pip install -r requirements.txt # optional: download again
```

Create a Python file `flappy_bird_tutorial.py`, which we will be working from:

```sh
echo > flappy_bird_tutorial.py
```

```py
# flappy_bird_tutorial.py
import pygame
import neat-python
import time
import os
import random
```

Ensure this runs by heading into the terminal with the virtual environment running:

```sh
python flappy_bird_tutorial.py
```

Save these files and update git before beginning the project:

```sh
cd flappy_bird_ai

git status
git add .
git commit -m "Completed project setup"
git push -u origin main
git status
git log --oneline
q
```

## Tech With Tim - Python Flappy Bird AI Tutorial (with NEAT)

### Video 1: Creating the Bird

Let's start by programming the game and getting the graphics looking good, before doing anything with the AI.

We need to import 2 modules:
- pygame: cross-platform set of Python modules designed for writing video games
    - Has computer graphics
- neat-python: NEAT is a method developed by Kenneth O. Stanley for evolving arbitrary neural networks.
    - NEAT-Python is a pure Python implementation of NEAT, with no dependencies other than the Python standard library.

Next, we need the images for this game. They can be found at this link:

[Link to download images](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbUZSU1ZwSkxCZ0ZZdldBZVhRamJpVUpoSlBYQXxBQ3Jtc0tuQWxoSnA1N3hWbnZTVFB1cUFmbzFMNDA1bGNBUzl2cGtQTG9BYzZLTU5yRGpodTJySDRYWW96UE4xY3IwYmVESFVqLTgwTFJuVmFJaXVDNTRhcUtuMjdyV1BNalowLV8zUlpWaFQtaUdSUlV2VW9jZw&q=https%3A%2F%2Fdev-cms.us-east-1.linodeobjects.com%2Fimgs_b286d95d6d.zip&v=MMxFDaIOHsE)

After downloading the .zip file, unzip its contents, and place the folder `imgs` inside of our root directory of `flappy_bird_ai`.

Next, let's open up the Python Script (flappy_bird_tutorial.py) in Sublime Text, and begin coding:

```py
WIN_WIDTH = 600 # Use all capitals for constants!
WIN_HEIGHT = 800

BIRD_IMGS = [
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
```

Notes:
- We wanted to start figuring out aspects of the game that we need. We are going to be using an object oriented programming approach, with these as our objects that we need classes for:
    - Pipe
    - Bird
    - Ground

- pygame.image.load: Loads an image 
- pygame.transform.scale2x: Doubles the size of the image
- 

You can check that your code is working with no errors by running it in the virtual environment:

```sh
python flappy_bird_tutorial.py
```

What the python file looks like at the end of the video:

```py
import pygame
import neat
import time
import os
import random

# LOAD IN ALL IMAGES, SET DIMENSIONS FOR SCREEN
print("setting dimensions...")

WIN_WIDTH = 600 # Use all capitals for constants!
WIN_HEIGHT = 800

print("loading images...")

BIRD_IMGS = [
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# BEGIN WRITING CLASSES

print("writing classes...")

class Bird:
	# constant class vars
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25 # DEGREES - HOW MUCH BIRD CAN TILT (NOSE TO SKY)
	ROT_VEL = 20 # HOW MUCH TO ROTATE EACH FRAME
	ANIMATION_TIME = 5 # HOW FAST BIRD FLAPS WINGS IN THE FRAME

	def __init__(self, x, y):
		# starting position
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0 # velocity
		self.height = self.y # talk about this later
		self.img_count = 0 # shows image we are currently using
		self.img = self.IMGS[0] # bird 1 gets loaded in

	# jump: when bird flaps up
	def jump(self):
		self.vel = -10.5 # this works - value is negative because 0,0 (top left) means in order to go up, we need negative velocity in y direction
		self.tick_count = 0 # keep track of when we last jumped (reset to 0 to know when changing directions / used by physics formulas)
		self.height = self.y # where the bird jumped / started moving from

	# called every frame to move bird
	# - think of while loop that gets called 30 times every 1 second (30 fps/frames per second)
	def move(self):
		self.tick_count += 1 # a frame went by, we have moved, so keep track of how many times we moved since last jump

```

Updating Git repo:

```sh
cd flappy_bird_ai

git status
git add .
git commit -m "Completed Video #1 - Creating the Bird"
git push -u origin main
git status
git log --oneline
q
```

### Video 2: Moving Birds

Current state of code:

Updates to the code:

```py

```

Note: Once we get the code to run and the game to load up, our flappy bird falls very quickly.
- The fix? Implementing a clock.

Updating git repo:

```sh
cd flappy_bird_ai

git status
git add .
git commit -m "Completed Video #2 - Moving Birds"
git push -u origin main
git status
git log --oneline
q
```


### Video 3: Pixel Perfect Collision w/ Pygame

### Video 4: Finishing the Graphics

### Video 5: NEAT Configuration and Explanation

### Video 6: Implementing NEAT/Creating Fitness Function

### Video 7: Finishing Touches and Testing