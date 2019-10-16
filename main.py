from math import sin, cos

import pygame
import time
pygame.init()
comicSans = pygame.font.SysFont('Comic Sans MS', 30)
WIDTH = 600
HEIGHT = 450

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Hyperbolic Jump Chamber')
runGame = True

APPROACH_RATE = 600 #ms
HIT_TOLERANCE = 150 #ms
CIRCLE_SIZE = 7 #% of screen height

class HitCircle:
    def __init__(self, size, x, y, time):
        self.radius = size
        self.x = x
        self.y = y
        self.time = time
        self.visible = False;


def generate_hit_circles(amount, circleTimePeriod = 500):
    hit_circle_list = list()
    for i in range(amount):
        x = int(sin(2.4*i)*150 + WIDTH/2)
        y = int(cos(2.4*i)*150 + HEIGHT/2)
        radius = int((CIRCLE_SIZE/100)*HEIGHT)
        hit_circle = HitCircle(radius, x, y, (i+1)*circleTimePeriod)
        hit_circle_list.append(hit_circle)
    return hit_circle_list

def render(visible_circles):
    display.fill(BLACK)
    for circle in visible_circles:
        #hit circle
        pygame.draw.circle(display, WHITE, (circle.x, circle.y), circle.radius, int(circle.radius/10))
        #approach circle
        time_difference = circle.time - abs_time
        if time_difference < 0:
            time_difference = 0
        approach_radius = int(circle.radius*(1 + 3*(time_difference/APPROACH_RATE)))
        pygame.draw.circle(display, WHITE, (circle.x, circle.y), approach_radius, int(circle.radius / 10))
    #Draw FPS
    textsurface = comicSans.render("FPS:{0}".format(int(1/delta_time)), False, WHITE)
    display.blit(textsurface, (0, 0))
    pygame.display.flip()

hit_circles = generate_hit_circles(100, 400)
start_time = time.time()
last_time = start_time
while runGame:
    current_time = time.time()
    abs_time = (current_time - start_time)*1000.0 #ms
    delta_time = current_time - last_time
    last_time = current_time
    #print("Delta time:{0}ms FPS:{1}".format(delta_time*1000, 1/delta_time))
    #Figure out which circles are visible at the time for rendering and gameplay
    visible_circle_list = list()
    for circle in hit_circles:
        time_difference = circle.time - abs_time
        if time_difference < -HIT_TOLERANCE:
            hit_circles.remove(circle)
        elif time_difference < APPROACH_RATE:
            visible_circle_list.append(circle)


    # Listen for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    #render visible circles
    render(visible_circle_list)

pygame.quit()
quit()