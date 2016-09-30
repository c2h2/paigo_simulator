import sys
import datetime
import pygame
import time
import random
import math

FPS=60

ms=0
seconds=0
minutes=0
uptime=0
diff_ms=0

pygame.init()
clock = pygame.time.Clock()
width = 800
height =800

screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Arial', 15)
black = (0,0,0)

'''constatnt'''
alex_width = 0.098


'''we want some motion related global variables'''
pwm_l=0
pwm_r=0
required_pwm_l=0
required_pwm_r=0

required_speed_l=0
required_speed_r=0
speed_l=0
speed_r=0

odo_l=0
odo_r=0

steps_l=0
steps_r=0

pos_x=0
pos_y=0
pos_theta=0
goal_x=0
goal_y=0


def init():
    global pos_x, pos_y, width, height
    #pos_x = width/2.0
    #pos_y = height/2.0


def set_pwm(l,r):
    pass

def set_goal(x,y,theta):
    pass

def _update_bot_speed():
	global speed_l, speed_r, required_speed_l, required_speed_l
	speed_l = required_speed_l
	speed_r = required_speed_r


def _update_physics():
    global diff_ms, alex_width, pos_x, pos_y, pos_theta
    icc_r = (alex_width/2.0) * (speed_l + speed_r) / (speed_r - speed_l + 0.000001) 
    '''+0.000001 is for divide by zero '''
    icc_omega = (speed_r - speed_l) / alex_width
    avg_speed = (speed_l + speed_r) / 2 
    pos_theta += icc_omega * diff_ms / 1000.0
    pos_theta = pos_theta % (2* math.pi)
    pos_x += avg_speed * diff_ms / 1000.0 * math.cos(pos_theta)
    pos_y += avg_speed * diff_ms / 1000.0 * math.sin(pos_theta)


def _clear_screen():
    screen.fill((255,255,255))

def _update_text():
    global minutes, seconds, ms, width, diff_ms, pos_theta
    y_text_pos = 5
    text ="uptime: {}m{}s {}\"".format(minutes, seconds, ms)
    screen.blit(font.render(text, True, black), (width - 100, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("diff: {} ms".format(diff_ms), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_l: {} m/s".format(required_speed_l), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_r: {} m/s".format(required_speed_r), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_x: {} m".format(pos_x), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_y: {} m".format(pos_y), True, black), (width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_theta: {} rad".format(pos_theta), True, black), (width - 150, y_text_pos))
    
    


def _draw_bot():
    global pos_x, pos_y, pos_theta, wdith, height
    color = (200,200,200)
    radius = 5
    ratio = 10.0
    pix_x = int(pos_x * ratio+ width / 2.0)
    pix_y = int(height / 2.0 - pos_y * ratio)
    pygame.draw.circle(screen, color, (pix_x,pix_y), radius*2)
    pygame.draw.line(screen, (200, 0, 0), (pix_x, pix_y), (pix_x+math.cos(pos_theta)*(radius+1), pix_y-math.sin(pos_theta)*(radius+1)))


def update_world():
    _update_bot_speed()
    _update_physics()
    _clear_screen()
    _update_text()
    _draw_bot()
    pygame.display.update()


def run():
    global ms, seconds, minutes, uptime, pos_x, pos_y, required_speed_l, required_speed_r, diff_ms
    

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
                    required_speed_l += 0.05
                if event.key == pygame.K_u:
                    required_speed_r += 0.05
                if event.key == pygame.K_v:
                    required_speed_l -= 0.05
                if event.key == pygame.K_n:
                    required_speed_r -= 0.05
                if event.key == pygame.K_f:
                    required_speed_l = 0
                if event.key == pygame.K_j:
                    required_speed_r = 0


        update_world()

        diff_ms = clock.tick_busy_loop(FPS)
        ms += diff_ms
        uptime += diff_ms

'''program entry here'''
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
