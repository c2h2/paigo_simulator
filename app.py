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
screen_width = 800
screen_height =800

screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont('Arial', 16)
black = (0,0,0)

'''constatnt'''
alex_screen_width = 0.098
object_mass = 1.0
pwm_acc_rate = 1/500.0

'''we want some motion related global variables'''
pwm_l=0
pwm_r=0

'''reistance in pwm'''
resistance_l=20
resistance_r=20

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

icc_r = 0
icc_omega =0 

'''
Physics:

pwm affects electirc current
electric current = (pwm * voltage - backEMF) / wire impedance
electric current = output force - powertrain resistance

f = force - friction or resistance
f = m * a
v = intergal a dt
d = intergal v at

more physics at _update_physics

'''


def init():
    global pos_x, pos_y, screen_width, screen_height, resistance_l, resistance_r
    #pos_x = screen_width/2.0
    #pos_y = screen_height/2.0


def control_pwm():
    global speed_l, speed_r, required_speed_l, required_speed_l, pwm_l, pwm_r
    learning_rate = 0.5
    error_speed_l = required_speed_l - abs(speed_l)
    error_speed_r = required_speed_r - abs(speed_r)

    pwm_l += error_speed_l / 0.5 * learning_rate
    pwm_r += error_speed_l / 0.5 * learning_rate

    if pwm_l > 255:
        pwm_l = 255
    if pwm_r > 255:
        pwm_r = 255


def set_goal(x,y,theta):
    pass

def _update_bot_speed():
    global speed_l, speed_r, required_speed_l, required_speed_r, diff_ms


    speed_l = required_speed_l
    speed_r = required_speed_r
    return

    #TODO fix this function below
   
    #resistance in accelation m/s2, consists of constant + a factor of speed due to transmission loss and random surface friction.
    #simulate resistance
    acc_l = pwm_l * pwm_acc_rate - speed_l * ( 0.1 + random.uniform(0.05, 0.2)) - 0.01
    acc_r = pwm_r * pwm_acc_rate - speed_r * ( 0.1 + random.uniform(0.05, 0.2)) - 0.01

    if(abs(required_speed_l) < 0.01 and abs(required_speed_r) < 0.01):
        return 


    if(speed_l < 0):
        speed_l -= acc_l * diff_ms / 1000.0
    #elif(abs(speed_l) < 0.02):
    #    speed_l = 0.0
    else:
        speed_l += acc_l * diff_ms / 1000.0

    if(speed_r < 0):
        speed_r -= acc_r * diff_ms / 1000.0
    #elif(abs(speed_r) < 0.02):
    #    speed_r = 0.0
    else:
        speed_r += acc_r * diff_ms / 1000.0


    control_pwm()



def _update_physics():
    global diff_ms, alex_screen_width, pos_x, pos_y, pos_theta, icc_r, icc_omega
    diff_s = diff_ms / 1000.0
    icc_r = (alex_screen_width/2.0) * (speed_l + speed_r) / (speed_r - speed_l + 0.00000001) 
    icc_omega = (speed_r - speed_l) / alex_screen_width
    avg_speed = (speed_l + speed_r) / 2 
    pos_theta += icc_omega * diff_s
    pos_theta = pos_theta % (2* math.pi)
    pos_x += avg_speed * diff_s * math.cos(pos_theta)
    pos_y += avg_speed * diff_s * math.sin(pos_theta)


def _clear_screen():
    screen.fill((255,255,255))

def _update_text():
    global minutes, seconds, ms, screen_width, diff_ms, pos_theta, pwm_l, pwm_r,speed_r,speed_l, icc_omega, icc_r
    y_text_pos = 5
    text ="uptime: {}m{}s {}\"".format(minutes, seconds, ms)
    screen.blit(font.render(text, True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("diff: {} ms".format(diff_ms), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_l: {} m/s".format(required_speed_l), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("req_speed_r: {} m/s".format(required_speed_r), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_x: {} m".format(round(pos_x,3)), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_y: {} m".format(round(pos_y,3)), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pos_theta: {} rad".format(round(pos_theta,3)), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("v_l: {} m/s".format(speed_l), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("v_r: {} m/s".format(speed_r), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pwm_l: {}".format(pwm_l), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("pwm_r: {}".format(pwm_r), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("icc_omega: {} rad/s".format(round(icc_omega,3)), True, black), (screen_width - 150, y_text_pos))
    y_text_pos+=10
    screen.blit(font.render("icc_r: {} m".format(round(icc_r,3)), True, black), (screen_width - 150, y_text_pos))
    
    


def _draw_bot():
    global pos_x, pos_y, pos_theta, screen_wdith, screen_height, icc_r
    color = (200,200,200)
    radius = 5
    ratio = 40.0
    pix_x = int(pos_x * ratio+ screen_width / 2.0)
    pix_y = int(screen_height / 2.0 - pos_y * ratio)

    #rulers
    ruler_color = (200,200,200)
    pygame.draw.line(screen, ruler_color, (0, screen_height/2), (screen_width, screen_height/2))
    pygame.draw.line(screen, ruler_color, (screen_width/2, 0), (screen_width/2, screen_height))
    screen.blit(font.render("{} m".format(round(screen_width/2/ratio),3), True, ruler_color), (screen_width - 40, screen_height/2+10))
    screen.blit(font.render("{} m".format(round(-screen_width/2/ratio),3), True, ruler_color), (10, screen_height/2+10))
    screen.blit(font.render("{} m".format(round(screen_height/2/ratio),3), True, ruler_color), (screen_width/2 + 10, 5))
    screen.blit(font.render("{} m".format(round(-screen_height/2/ratio),3), True, ruler_color), (screen_width/2 + 10, screen_height-20))
    

    # bot
    pygame.draw.circle(screen, color, (pix_x,pix_y), radius*2)
    pygame.draw.line(screen, (200, 0, 0), (pix_x, pix_y), (pix_x+math.cos(pos_theta)*(radius+1), pix_y-math.sin(pos_theta)*(radius+1)))
    
   

    #trajectory
    traj_color =  (50, 200, 50)
    if icc_r > 100 and (speed_l > 0 or speed_r > 0):
        pygame.draw.line(screen, traj_color, (pix_x+math.cos(pos_theta)*(radius+3), pix_y-math.sin(pos_theta)*(radius+3)),(pix_x+math.cos(pos_theta)*(radius+1000), pix_y-math.sin(pos_theta)*(radius+1000)))
    
    if abs(icc_r * ratio) > 1 and abs(icc_r) < 100:
        pygame.draw.circle(screen, traj_color, (int(round(pix_x - math.sin(pos_theta)*(icc_r*ratio))), int(round(pix_y-math.cos(pos_theta)*(icc_r*ratio)))), int(round(abs(icc_r*ratio))), 1)


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

        speed_step = 0.01

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    required_speed_l += speed_step
                if event.key == pygame.K_u:
                    required_speed_r += speed_step
                if event.key == pygame.K_v:
                    required_speed_l -= speed_step
                if event.key == pygame.K_n:
                    required_speed_r -= speed_step
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
