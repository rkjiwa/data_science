## the main program

# imports
import pygame
pygame.font.init()
import neat
import time
import os
import random
import classes

# define constants
WIN_WIDTH = 500
WIN_HEIGHT = 800

UFO_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","ufo.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","space.png")))
BLOCK_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","belt.png")))
OBSTACLE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","belt.png")))
STAT_FONT = pygame.font.SysFont("helveticaneuettc",50)

# draw the game window
def draw_window(win, ufos, obstacles, score):
    win.blit(BG_IMG,(0,0))
    #draw the obstacles
    for obstacle in obstacles:
        obstacle.draw(win)

# obtain and print the score
    text= STAT_FONT.render("Score: "+ str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH-10-text.get_width(),10))

    #draw the ufos
    for ufo in ufos:
        ufo.draw(win)

    pygame.display.update()




# implementation of the genetic algorithm
def main(genomes, config):
    nets=[]
    ge=[]
    ufos=[]

# loop through each of the genomes
    for _, g in genomes:
        # set the nets from the neat algorithm
        net=neat.nn.FeedForwardNetwork.create(g,config)
        # add the nets to the list
        nets.append(net)
        # create the ufos
        ufos.append(classes.Ufo(230,350))
        # set the starting fitness for the ufos
        g.fitness=0
        ge.append(g)

    # create the first obstacle
    obstacles=[classes.Obstacle(500)]
    #window display
    win=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock= pygame.time.Clock()

    score=0

    run= True
    while run:
        # set the frames per second
        clock.tick(30)
        # set a quitting condition for the run
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run=False
                pygame.quit()
                quit()

        #obstacle index
        obstacle_ind=0
        # if there is still a ufo present
        if len(ufos)>0:
            if len(obstacles)>1 and ufos[0].x > obstacles[0].x+obstacles[0].OBSTACLE_TOP.get_width():
                obstacle_ind=1
        else:
            run=False
            break

        for x, ufo in enumerate(ufos):
            ufo.move_2()
            ge[x].fitness+=0.1

            # utilize the neural net, inputting the position of the ufos and the position of the obstacles
            output=nets[x].activate((ufo.y,abs(ufo.y-obstacles[obstacle_ind].height), abs(ufo.y-obstacles[obstacle_ind].bottom)))
            # based off of the different outputs, select the options for the ufo's movement
            if output[0] > 0.3 and output[0] <= 1:
                ufo.jump()
            #elif output[0] > -0.5 and output[0] <= 0.5:
            #    ufo.stay()
            elif output[0] >= -1 and output[0] <= 0.3:
                ufo.fall()

        #
        add_obstacle=False
        rem=[]

        for obstacle in obstacles:
            for x, ufo in enumerate(ufos):
                # if the ufo collides with the obstacle
                if obstacle.collide(ufo):
                    # decrease the fitness
                    ge[x].fitness-=1
                    # remove the x from the list
                    ufos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # check if another obstacle needs to be added
                if not obstacle.passed and obstacle.x <ufo.x:
                    obstacle.passed =True
                    add_obstacle= True

            if obstacle.x+obstacle.OBSTACLE_TOP.get_width()<0:
                rem.append(obstacle)


            obstacle.move()

        if add_obstacle:
            score+=1
            for g in ge:
                g.fitness+=5

            obstacles.append(classes.Obstacle(550))

        for r in rem:
            obstacles.remove(r)

        #each ufo hitting the ground and ceiling
        for x, ufo in enumerate(ufos):
            if ufo.y + ufo.img.get_height()>=800 or ufo.y<0:
                ufos.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, ufos, obstacles, score)



# to run the main generations
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stats reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

import sys
if __name__=="__main__":
    local_dir=os.path.dirname(sys.argv[0])
    config_path='/Users/rahimjiwa/Documents/DataScience/space/NEAT_config.txt'
    run(config_path)
