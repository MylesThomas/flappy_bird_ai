import pygame
import neat
import time
import os
import random
pygame.font.init() # fixes error: "pygame.error: font not initialized"

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

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50) # create a Font object from the system fonts


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
	def collide(self, bird):
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
def draw_window(win, bird, pipes, base, score):
	win.blit(BG_IMG, (0,0)) # blit = draw on the window ; (0,0) = top left of screen

	# pipes: list (we can have more than 1 pipe on the screen at once)
	for pipe in pipes:
		pipe.draw(win)

	# font to tell us the score
	text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255)) # (255,255,255) = white
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

	# base: 1 base
	base.draw(win)

	# bird: 1 bird
	bird.draw(win)
	# 
	pygame.display.update()

# method: runs the main loop of our game
# - need: genomes, config
def main(genomes, config):
	# bird = Bird(230,350) # create a bird object
	# keep track of neural network that controlls each bird!
	# - need to know so we can change genomo fitness, based on how it performed
	nets = [] # 
	ge = []
	birds = []

	for g in genomes:
		# setup a neural network for each genome...
		# keep track of genome in a list
		# - all the lists will correspond with one another

		net = neat.nn.FeedForwardNetwork(g, config) # create net, make sure to give it the config file
		nets.append(net) # append to list
		birds.append(Bird(230, 350)) # append to list

		g.fitness = 0 # init fitness at 0 for each genome
		ge.append(g) # append to list


	base = Base(730) # base: bottom of screen at 730
	pipes = [Pipe(600)] # 1 pipe with height 600
	win = pygame.display.set_mode( (WIN_WIDTH, WIN_HEIGHT) ) # create window 
	clock = pygame.time.Clock() # create a clock object to _

	score = 0

	# create while loop for main game window
	run = True
	while run:
		clock.tick(30) # at MOST 30 ticks per second (makes the bird fall down slower!)
		# keeps track of when something happens ie. user clicks the mouse
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# this will quit pygame
				run = False

		# check for collision between Bird/Pipe
		add_pipe = False # variable to decide if we need to add a new pipe later
		rem = [] # list of pipes to remove
		for pipe in pipes:
			for x, bird in enumerate(birds):
				if pipe.collide(bird):
					# OLD: if a bird collides: end the game for that bird! and make sure the 
					ge[x].fitness -= 1 # when a bird hits a pipe, remove 1 from fitness score (don't reward birds who keep hitting pipes)
					birds.pop(x) # remove bird from screen
					nets.pop(x) # remove neural net
					ge.pop(x) # remove genome


				if not pipe.passed and pipe.x < birds.x:
					# check if birds have passed by the pipe
					pipe.passed = True
					add_pipe = True

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				# if pipe is off the screen, remove that pipe
				# - cannot remove from for loop, but we will add to a list to remove
				rem.append(pipe)

			# finally, move the pipe if we make it this far! (the bird has passed all of the pipes)
			pipe.move()

		if add_pipe:
			# we have passed a pipe, we need to add more pipes.
			# - we have also scores, so increment that variable too
			score += 1 # increment score
			# increase fitness score for getting through the pipe (encourage them to go through the pipe!!)
			for g in ge:
				g.fitness += 5
			pipes.append(Pipe(600)) # add a new pipe

		
		for r in rem:
			# remove the pipes that we don't need anymore...
			pipes.remove(r) 

		# Check if any of the birds hit the ground
		for x, bird in enumerate(birds):
			if bird.y + bird.img.get_height() >= 730:
				# if the bird hits the ground, pop from program/screen
				birds.pop(x)
				nets.pop(x)
				ge.pop(x)



		# These move functions: gets called every frame so bird can tick
		# (commented out since we have AI move the bird, not our keyboard.)
		#bird.move() # makes our bird fall down 
		base.move()  # makes the base move, so that our bird is flying along

		draw_window(win, bird, pipes, base, score)

	pygame.quit() # quit pygame
	quit() # quit program


# Call the main function
main()

# Method that 
def run(config_path):
	# load in the config
	config = neat.config.Config(
		# it assumes neat.NEAT, so no need to include that here
		neat.DefaultGenome, # define sub-headings
		neat.DefaultReproduction,
		neat.DefaultSpeciesSet,
		neat.DefaultStagnation,
		config_path,
	)

	# generate a population, based on what is in the config file
	p = neat.Population(config)

	# create stats reporters (gives us output when we are running the algorithm, think verbose in command line)
	p.add_reporter(neat.StdOutReporter(True)) # gives stats
	# 
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	# choose winner / setting fitness function
	# - fitness function: how far it moves in the game
	# - this makes main() the fitness function (it gets called 50 times, passes all of the Genome + config file)
	winner = p.run(main, 50) # 50 = 50 generations


if __main__ == "__main__":
	# 
	local_dir = os.path.dirname(__file__) # gives path to the directory we are in (need to load in config file)
	config_path = os.path.join(local_dir, "config-feedforward.txt") # config path

	run(config_path)