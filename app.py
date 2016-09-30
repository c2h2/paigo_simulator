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
width = 800
height =800

screen = pygame.display.set_mode((width, height))
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

odo_l=0
odo_r=0

steps_l=0
steps_r=0

pos_x=0
pos_y=0
goal_x=0
goal_y=0


def init():
    pass

def set_speed(l,r):
    required_speed_l = l
    required_speed_r = r

def set_pwd(l,r):
    pass

def set_goal(x,y,theta):
    pass

def _update_bot_speed():
	pass

def _update_bot_pos():
    return 1,2,3

def _clear_screen():
    screen.fill((255,255,255))

def _add_clock():
    global minutes, seconds, ms, width
    y_text_pos = 5
    text ="uptime: {}m{}s {}\"".format(minutes, seconds, ms)
    screen.blit(font.render(text, True, black), (width - 100, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_l: {} m/s".format(required_speed_l), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_r: {} m/s".format(required_speed_r), True, black), (width - 150, y_text_pos))


def _draw_bot():
    global pos_x, pos_y
    color = (200,200,200)
    radius = 5
    pygame.draw.circle(screen, color, (pos_x,pos_y), radius*2)
    pygame.draw.line(screen, (100, 0, 0), (pos_x, pos_y), (pos_x+radius, pos_y))


def update_screen():
    _clear_screen()
    _add_clock()
    x, y, theta = _update_bot_pos()
    _draw_bot()
    pygame.display.update()


def run():
    global ms, seconds, minutes, uptime, pos_x, pos_y, required_speed_l, required_speed_r
    

    while True: #game loop
        if ms > 1000:
            seconds += 1
            ms -= 1000
        if seconds > 60:
            minutes += 1
            seconds -= 60

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    required_speed_l += 1
                if event.key == pygame.K_u:
                    required_speed_r += 1
                if event.key == pygame.K_v:
                    required_speed_l -= 1
                if event.key == pygame.K_n:
                    required_speed_r -= 1
                if event.key == pygame.K_f:
                    required_speed_l = 0
                if event.key == pygame.K_j:
                    required_speed_r = 0


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
