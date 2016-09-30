import sys
import datetime
import pygame
import time
import random

FPS=25

ms=0
seconds=0
minutes=0
uptime=0

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
font = pygame.font.SysFont('Arial', 15)
black = (0,0,0)

'''we want some motion related global variables'''
pwm_l=0
pwm_r=0
required_pwm_l=0
required_pwm_r=0
required_speed_l=0
required_speed_r=0
actual_speed_l=0
actual_speed_r=0



def init():
    pass

def set_speed(l,r):
    required_speed_l = l
    required_speed_r = r

def set_pwd(l,r):
    pass

def set_goal(x,y,theta):
    pass


def _update_bot_pos():
    return 100, 100, 0


def _clear_screen():
    screen.fill((255,255,255))

def _add_clock():
    global minutes, seconds, ms
    text ="uptime: {}m{}s {}\"".format(minutes, seconds, ms)
    screen.blit(font.render(text, True, black), (700, 5))

def _draw_bot(x, y, theta):
    color = (200,200,200)
    posx,posy = x,y
    radius = 5
    pygame.draw.circle(screen, color, (posx,posy), radius*2)
    pygame.draw.line(screen, (100, 0, 0), (posx, posy), (posx+radius, posy))


def update_screen():
    _clear_screen()
    _add_clock()
    x, y, theta = _update_bot_pos()
    _draw_bot(x,y,theta)
    pygame.display.update()


def run():
    global ms, seconds, minutes, uptime
    

    while True: #game loop
        if ms > 1000:
            seconds += 1
            ms -= 1000
        if seconds > 60:
            minutes += 1
            seconds -= 60

        update_screen()

        diff = clock.tick_busy_loop(FPS)
        ms += diff
        uptime += diff


init()
run()



'''unused'''

def tick_100():
    print "tick 100"

def tick_1000():
    print "tick 1000"


'''
comment
    tick = 1
    while True:
        if (tick % 100 ==0):
            tick_100()

        if (tick % 1000 == 0):
            tick_1000()
            update_screen()

        tick+=1
        time.sleep(0.001)
'''
