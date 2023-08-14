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
