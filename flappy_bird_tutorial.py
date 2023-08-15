import pygame
import neat
import time
import os
import random

# LOAD IN ALL IMAGES, SET DIMENSIONS FOR SCREEN
print("setting dimensions...")

WIN_WIDTH = 500 # Use all capitals for constants!
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

		# displacement - how many spaces we move up/down this frame
		# - what we move when y position changes
		# (as soon as we jump, we reset tick count to 0, so when tick count is 1, we have this: -10.5 + 1.5 = -9)
		d = self.vel*self.tick_count + 1.5*self.tick_count**2

		# if we are moving down more than 16 pixels, set it at 16 (so we don't move down too fast!)
		if d >= 16:
			d = 16

		# if we are moving upwards, just move up a little bit more
		# - you can edit this, but this is a solid start for the jump height
		if d < 0:
			d -= 2

		# 
		self.y = self.y + d 

		# see if we are tilting up/tilting down
		if d < 0 or self.y < self.height + 50:
			# as soon as we get below the point, start curving down
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION

		# 
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL


	def draw(self, win):
		"""
		win = window we are drawing the bird onto
		"""
		# to animate the bird, we must keep track of # of ticks we showed the image for
		self.img_count += 1

		# which image to show based on image count?
		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0 # reset image count

		# check one more condition
		# - we do not want the bird flapping its wings when we jump back up
		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		# rotate bird around center based on current tilt (this is kind of complicated)
		rotated_image = pygame.transform.rotate(self.img, self.tilt) # this rotates image for us
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) # rotate image around center
		win.blit(rotated_image, new_rect.topleft) # weird, but how to rotate image in pygame

	# use this for collisions
	def get_mask(self):
		return pygame.mask.from_surface(self.img) # we will talk about 'mask' later


# Class #2: The pipe
class Pipe:
	GAP = 200 # space between pipe
	VEL = 5 # how fast our pipe will be moving (bird doesn't move, all of the objects on the screen are moving!)

	def __init__(self, x): # why x and no y? the height of the tubes/where they show on the screen is randomized when a pipe is initialized!
		self.x = x
		self.height = 0
		# self.gap = 100

		# keeps track of where top AND bottom of the pipe is drawn
		# - also getting images for top/bottom pipe
		# - (must keep track of specific images, as we need vertical pipe and upside down pipe)
		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		# if the bird is passed by the pipe (for collision purposes/AI)
		self.passed = False
		self.set_height() # where top/bottom/height is (randomly defined)

	def set_height(self):
		# get random number for where type should be
		self.height = random.randrange(50, 450)
		self.top = self.height - self.PIPE_TOP.get_height() # figure out top/left position (draw pipe at negative location so that bottom is in correct spot)
		self.bottom = self.height + self.GAP

	# easiest method: move (all we need to do is move the x position, based on velocity per frame)
	def move(self):
		self.x -= self.VEL

	# draw: will draw top and bottom
	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	# most difficult: pixel perfect collision
	# - we draw boxes around each of our objects, check if they collide
	# - (can be problematic, because)
	def collide(self, bird, win):
		# what a mask does: tells if any of the pixels in the boxes are actually touching/colliding 
		bird_mask = bird.get_mask()
		# create mask for top pipe AND bottom pipe
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
		# offset: how far the top left corners/masks are from each other (checks pixels up against each other)
		top_offset = (self.x - bird.x, self.top - round(bird.y)) # round bc you cannot have negative values
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
		# figure out if masks collide by finding point of collision
		b_point = bird_mask.overlap(bottom_mask, bottom_offset) # if they don't collide: function returns None
		t_point = bird_mask.overlap(top_mask, top_offset) # if they don't collide: function returns None

		if t_point or b_point: # if either is not None...
			return True # collision! do something ie. make the bird die!
		else:
			return False # no collision - keep going

# we need a class for base because it is going to be moving at the bottom
class Base:
	VEL = 5 # needs to be same as pipe!
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y): # x is moving to left, don't need to define that
		self.y = y
		self.x1 = 0 # at 0 
		self.x2 = self.WIDTH # directly behind the image

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		# What goes on here:
		# - we are drawing 2 images for the base (they move at same VEL, so looks like 1 image)
		# - when 1 image is totally off the screen and one is totally on, the one that is off, cycles to the back
		# - (think of a circle of the 2 images moving)

		# is it off the screen?
		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		# is it off the screen?
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))
		

# method: draws window of our game
def draw_window(win, bird):
	win.blit(BG_IMG, (0,0)) # blit = draw on the window ; (0,0) = top left of screen
	bird.draw(win)
	pygame.display.update()

# method: runs the main loop of our game
def main():
	bird = Bird(200,200) # create a bird object
	win = pygame.display.set_mode( (WIN_WIDTH, WIN_HEIGHT) ) # create window 
	clock = pygame.time.Clock() # create a clock object to _

	# create while loop for main game window
	run = True
	while run:
		clock.tick(30) # at MOST 30 ticks per second (makes the bird fall down slower!)
		# keeps track of when something happens ie. user clicks the mouse
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# this will quit pygame
				run = False

		# gets called every frame so bird can tick
		bird.move()
		draw_window(win, bird)

	pygame.quit() # quit pygame
	quit() # quit program


# Call the main function
main()