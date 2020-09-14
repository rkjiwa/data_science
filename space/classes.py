# classes for space game

# imports
import pygame
import os
import time
import neat
import random

# images
UFO_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","ufo.png")))
OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","belt.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","space.png")))
BLOCK_IMG = pygame.image.load(os.path.join("imgs","belt.png"))

# class for ufos
class Ufo():
    IMGS=UFO_IMGS

    def __init__(self,x,y):
        #ufo start poisition
        self.x = x
        self.y = y
        self.tick_count =0
        self.vel =0
        self.height = self.y
        self.img_count = 0
        self.img=self.IMGS

# mechanism for upward movement
    def jump(self):
        self.vel = -8
        self.tick_count = 0
        self.y += self.vel

# function to move the ufo
    def move_2(self):
        self.tick_count += 1
        d = self.vel * self.tick_count
        self.y = self.y + d

# function to move the ufo while keeping its position the same
    def stay(self):
        self.vel = 0
        self.tick_count = 0
        self.y += self.vel

# function to move the ufo downwards
    def fall(self):
        self.vel = 8
        self.tick_count = 0
        self.y += self.vel

# draw the ufo
    def draw(self, win):
        win.blit(self.img,(self.x, self.y) )

# function to get the mask of the ufo that can be used to determine collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# class object for the obstacles
class Obstacle():
    # the gap between the asteroid belt
    GAP = 200
    # movement speed
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        # where the top and bottom of the obstacle is
        self.top = 0
        self.bottom = 0

        # flip image to create the other side
        self.OBSTACLE_TOP = pygame.transform.flip(OBSTACLE_IMG, False, True)
        self.OBSTACLE_BOTTOM = OBSTACLE_IMG
        # create block
        self.block = BLOCK_IMG
        self.blocktype = random.choice(['obstacle','block'])
        # randomize the initial poing for the blocks
        self.y = random.randrange(100,300)

        self.passed = False

        self.set_height()

    # to set the height of the different obstacles
    def set_height(self):
        #since we have two different types of objects, we needs to set the heigh differently for each object
        # this checks if the obstacle is a belt
        # it  picks a random height for it, and then it gets the height for the top
        if self.blocktype == 'obstacle':
            self.height = random.randrange(50, 450)
            self.top = self.height - self.OBSTACLE_TOP.get_height()
            self.bottom = self.height + self.GAP
        # the second type of object is an asteriod block
        # this sets the top which was randomly chosen
        # the bottom is set by adding the size of the asteroid block
        else:
            self.block_top = self.y
            self.block_bottom = self.top + 350

    # this moves the obstacles
    def move(self):
        self.x -= self.VEL

    # draws the obstacles in the window
    def draw(self, win):
        # condition if it is the asteroid belt object
        if self.blocktype == 'obstacle':
        # draw top
            win.blit(self.OBSTACLE_TOP, (self.x, self.top))
        # draw bottom
            win.blit(self.OBSTACLE_BOTTOM, (self.x, self.bottom))
        # draw the asteroid block
        else:
            win.blit(self.block, (self.x, self.y))


    # this is the collision mechanism to determine if a collision occurred.
    def collide(self, ufo):
        #Pixel perfect collision
        ufo_mask = ufo.get_mask()
        if self.blocktype == 'obstacle':
            top_mask = pygame.mask.from_surface(self.OBSTACLE_TOP)
            bottom_mask = pygame.mask.from_surface(self.OBSTACLE_BOTTOM)

        #Offset pixel count
            top_offset = (self.x - ufo.x, self.top - round(ufo.y))
            bottom_offset = (self.x - ufo.x, self.bottom - round(ufo.y))

            b_point = ufo_mask.overlap(bottom_mask, bottom_offset)
            t_point = ufo_mask.overlap(top_mask,top_offset)

            if b_point or t_point:
                return True
        # define the collision when the obstacle is a block
        elif self.blocktype == 'block':
            # get the pygame mask of the block
            block_mask = pygame.mask.from_surface(self.block)
            # check the top and bottom
            top_offset = (self.x - ufo.x, self.block_top - round(ufo.y))
            bottom_offset = (self.x - ufo.x, self.block_bottom - round(ufo.y))
            # check to see if the ufo mask and the block masks overlap
            b_point = ufo_mask.overlap(block_mask, bottom_offset)
            t_point = ufo_mask.overlap(block_mask,top_offset)
            # comes true if there is overlap
            if b_point or t_point:
                return True
        return False
