#!/bin/python3
#   Copyright(c) Jose Moran, jmoran071996@gmail.com
###################################################################
##
##   Fruit Ninja Demo in PyGame
##
##   Description: This is a basic Fruit Ninja demo intended to 
##   provide a testing GUI for usb-serial communication with
##   an analog accelerometer.
##
###################################################################

import pygame 
import math 
import random
import sys


xWin = 600
yWin = 600
img_path = 'images/'
fps = 16
win_size = (xWin,yWin)

pygame.display.set_icon(pygame.image.load(img_path+'icon.png'))
pygame.display.set_caption("Fruit Ninja")

fruit_list = {
    0:'watermelon',
    1:'banana',
    2:'peach',
    3:'basaha',
    4:'apple'
}

max_tail_size = 5

class knife:

    

    def __init__(self, win):
        self.pos = pygame.mouse.get_pos()
        self.drag = True
        self.win  = win
        self.tail_size = 0
        self.tail = []
        self.width = 7 
        self.height = 7
        self.default_size= (7,7)
        self.angle = 0
        self.enable_cut = False
        self.image = pygame.Surface(self.default_size)
        self.rect = self.image.get_rect()
        self.rect.top = self.pos[1]
        self.rect.bottom =  self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width
        self.flash = pygame.image.load(img_path + 'flash.png')

    def sharp(self):
        return self.enable_cut

    def enable_cutting(self):
        self.enable_cut = True

    def disable_cutting(self):
        self.enable_cut = False

    def draw(self):
        size = 7
        factor = 0.8
        if self.drag:
            for pos in reversed(self.tail):
                pygame.draw.rect(self.win,(255,255,255), (pos[0], pos[1], size, size))
                size = factor * size
                
    def find_angle(self):
        if len(self.tail) > 2:
            try: 
                self.angle = math.atan(abs((self.tail[-1][1]-self.tail[-2][1])/ (self.tail[-1][0] - self.tail[-2][0])))
            except:
                self.angle = math.pi / 2

            if self.tail[-1][1] < self.tail[-2][1] and self.tail[-1][0] > self.tail[-2][0]:
                self.angle = abs(self.angle)
            elif self.tail[-1][1] < self.tail[-2][1] and self.tail[-1][0] < self.tail[-2][1]:
                self.angle = math.pi - self.angle
            elif self.tail[-1][1] > self.tail[-2][1] and self.tail[-1][0] < self.tail[-2][0]:
                self.angle =  math.pi + abs(self.angle)
            elif self.tail[-1][1] > self.tail[-2][1] and self.tail[-1][0] > self.tail[-2][0]:
                self.angle = (math.pi * 2) - self.angle
            else:
                self.angle = 0
            

    def update_rect(self):
        self.rect.top = self.pos[1]
        self.rect.bottom =  self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width            


    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.update_rect()
        
        if self.tail_size < max_tail_size:
            self.tail.append(self.pos)
            self.tail_size +=1
        else:
            self.tail.pop(0) #pop firts element
            self.tail.append(self.pos)

        self.find_angle()
        #print(self.angle*180/math.pi)
        self.draw()
    
    def cut(self):
        rotatedFlash = pygame.transform.rotate(self.flash,self.angle*180/math.pi)
        rotflash = rotatedFlash.get_rect()
        rotflash.center = tuple(self.pos)
        self.win.blit(rotatedFlash,rotflash)
        



class fruit:

    def __init__(self, name, win, cut=False):
        self.name = name
        #print(self.name)
        self.image = pygame.image.load(img_path + name + '.png')
        self.rect = self.image.get_rect()
        self.width, self.height = self.image.get_size()
        
        self.cut = cut
        self.pos = [random.randint(self.width, xWin-self.width), yWin + (self.height+1)//2]
            

        self.update_rect()
        
        self.win = win
        self.destroy = False
        

        #physics configuration ---------------------------
        self.time = 0
        self.time_step = random.uniform(0.15, 0.2)
        self.spos = [self.pos[0], self.pos[1]]

        if self.pos[0] > (xWin//2):
            self.s_angle = random.uniform(math.pi/2, math.pi/2 + math.pi/18)
        else:
            self.s_angle = random.uniform( 4*math.pi/9, math.pi/2)
            
        self.speed = random.randint(int(0.14*yWin),int(0.16*yWin))
        self.svelx = self.speed*math.cos(self.s_angle)
        self.svely = -self.speed*math.sin(self.s_angle)

        self.time_limit = (-self.svely + math.sqrt(self.svely**2 + 16*self.spos[1])) / 8
        self.angle = 0
        if self.svelx > 0:
            self.angle_speed = -5
        else:
            self.angle_speed = 5


    def stop(self, angle=0):
        self.spos = [self.pos[0], self.pos[1]]
        self.time = 0
        self.s_angle = angle
        self.angle_speed = 1

        #--------------------------------------------------
    def change_image(self, name):
        self.image = pygame.image.load(img_path + name + '.png')

    def change_xspeed(self, speed):
        self.svelx = speed
        
    def change_yspeed(self):
        self.svely = speed

    def change_rot_speed(self, speed):
        self.angle_speed = speed

    def rotate(self, angle):
        self.angle = angle

    def update_rect(self):
        self.rect.top = self.pos[1]
        self.rect.bottom =  self.pos[1] + self.height
        self.rect.left = self.pos[0]
        self.rect.right = self.pos[0] + self.width
        
        
    def draw(self):
        rotatedSurf = pygame.transform.rotate(self.image,self.angle)
        rotFruit = rotatedSurf.get_rect()
        rotFruit.center = tuple(self.pos)
        self.win.blit(rotatedSurf,rotFruit)

    def physic(self):

        gravity = 5
        

        if (self.time <= self.time_limit):
            self.time += self.time_step
            self.pos[0] = self.spos[0] + self.svelx*(self.time)
            self.pos[1] = self.spos[1] + self.svely*(self.time) + (gravity*(self.time**2))
            
        else:
            self.destroy = True

    def update(self):
        
        self.angle = (self.angle + self.angle_speed) % 360   
        self.physic()
        self.update_rect()
        self.draw()


    #private

    def copy(self):
        newfr = fruit(self.name, self.win, self.cut)
        newfr.pos = self.pos
        newfr.update_rect()        

        #physics configuration ---------------------------
        newfr.time = self.time
        newfr.time_step = self.time_step
        newfr.spos = self.spos

        newfr.s_angle = self.s_angle
            
        newfr.speed = self.speed
        newfr.svelx = self.svelx
        newfr.svely = self.svely
        newfr.angle = self.angle
        return newfr        

def collision_handler(knf, frt):
    #case 1
    knife_angle = knf.angle
    fruit_angle = frt.angle 

    topFruit = frt.copy()
    topFruit.cut = True
    topFruit.change_image(topFruit.name + '-2')
        
    topFruit.svely = -0.3*fps/20* abs(topFruit.svely)

    botFruit = frt.copy()
    botFruit.cut = True
    botFruit.change_image(botFruit.name + '-1')
        
    botFruit.svely = -0.3*fps/20* abs(botFruit.svely)

    shoot_angle = math.pi/6
    new_vx = abs((0.08*yWin)*math.cos(shoot_angle))
    if (fruit_angle >= (2*math.pi - math.pi/2) and fruit_angle <= math.pi/2):
        topFruit.stop(shoot_angle)
        topFruit.rotate(2*math.pi - math.pi/2)
        botFruit.stop(math.pi - shoot_angle)
        botFruit.rotate(math.pi/2)


        topFruit.svelx = -new_vx
        botFruit.svelx = new_vx
    else: 
        topFruit.stop(math.pi - math.pi/18)
        topFruit.rotate(2*math.pi - math.pi/2)
        botFruit.stop(math.pi/18)
        botFruit.rotate(math.pi/2)
        topFruit.svelx = new_vx
        botFruit.svelx = -new_vx
        
    return topFruit,botFruit




def game_loop():

    #INITIAL SETTING 
    pygame.init()
    run = True 
    
    win = pygame.display.set_mode(win_size)

    
    background = pygame.image.load( img_path + 'background.png')
    knf = knife(win)
    fruits = []

    while True:
        num_fruits = random.randint(0,3)
        for i in range(num_fruits+1):
            option = random.randint(0,4)
            fruits.append(fruit(fruit_list[option], win))  


        while fruits != [] and run:     
            pygame.time.delay(fps)            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    knf.enable_cutting()
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    knf.disable_cutting()
                    

            
            
            win.blit(pygame.transform.scale(background,(xWin,yWin)),(0,0))
            knf.update()
            for fr in fruits:
                
                fr.update()
                
                
                if pygame.sprite.collide_rect(knf, fr) == True and knf.sharp() and not fr.cut:
                        top,bot = collision_handler(knf,fr)
                        fruits.append(top)
                        fruits.append(bot)
                        fruits.remove(fr)
                        knf.cut()
                        

                if fr.destroy == True:
                    fruits.remove(fr)
                

            
            pygame.display.flip()
        
        if not run:
            break



game_loop()