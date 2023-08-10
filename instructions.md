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

Note: neat-python used to be neat, so be aware of that if you are working from an older version of Python.

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

### Video 2: Moving Birds

### Video 3: Pixel Perfect Collision w/ Pygame

### Video 4: Finishing the Graphics

### Video 5: NEAT Configuration and Explanation

### Video 6: Implementing NEAT/Creating Fitness Function

### Video 7: Finishing Touches and Testing