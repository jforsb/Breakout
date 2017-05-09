# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 2015

@author: Julie Ehrlich and Jade Forsberg

In this project, we have created the game "breakout" with some special features:
1) Random colored bricks (they change color when hit)
2) Special bricks that change the size of the ball (random size) and color of the ball/paddle (random colors)
3) Change the velocity based on where the ball hits the bricks (left side decreases velocity, right side inceases velocity)
4) The cursor is not displayed on screen while we are playing
5) "VICTORY!!" message when the game is over
6) Score Keeper
7) "GAME OVER" message when the ball hits the floor
8) The paddle is controlled from the center

"""

from pyprocessing import *
import random

WIDTH = 600
HEIGHT = 500
RADIUS = 8


class Ball:
    """creates the ball"""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.vx = 8
        self.vy = 8
        

    def draw(self):
        #draw the ball
        ellipseMode(CENTER)
        fill(self.color[0], self.color[1], self.color[2])
        ellipse(self.x, self.y, self.radius*2, self.radius*2)
        
    def update(self, obstacles):
        #gives the ball velocity
        self.x += self.vx
        self.y += self.vy
        
        
        #bounce off the left or right wall
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.vx = - self.vx
            
        #bounce off the ceiling
        if self.y <= self.radius:
            self.vy = - self.vy 
            
        #ball hits the floor
        if self.y >= HEIGHT + self.radius:
            noLoop()                                #end the game
            cursor()                                #show cursor
            textSize(32)
            text('GAME OVER', 200, HEIGHT/2 + 100)  #display "Game Over" if ball hits the floor

            
            
        bounces = []
        for obstacle in obstacles:
            bounces.extend(obstacle.bounce(self))
            
        #if ball hits special brick 1, change the size randomly  
        if 'f' in bounces or 'g' in bounces or 'h' in bounces or 'i' in bounces :
            self.radius = RADIUS
            self.radius = self.radius + (random.randint(-10,10))
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            if self.radius >= 9: #sets maximum ball radius
                self.radius = 9
            if self.radius <= 4:  #sets minimum ball radius
                self.radius = 4
         
        #if ball hits top or bottom of brick, bounce off
        if 'b' in bounces or 't' in bounces:
            self.vy = -self.vy
            
        #if ball hits left or right of brick, bounce off
        if 'l' in bounces:
            self.vx = -self.vx + 3
            
        if 'r' in bounces:
            self.vx = -self.vx - 3
            
        #if the ball hits the top of the paddle, bounce off
        if 'tp' in bounces:
            self.vy = -self.vy
            
class Paddle:
    """create the paddle"""
    def  __init__(self, width, height, color):
        self.width = width
        self.height = height
        self. color = color
        self.x = WIDTH/2
        self.y = HEIGHT - self.height
      
      
    def draw(self):
        #draw the paddle
        rect(self.x,self.y,self.width,self.height)
        fill(self.color[0], self.color[1], self.color[2])
        
    def update(self):
        #paddle can move with the mouse (left/ right)
        self.x = mouse.x
        self.y = self.y
        
           
    def bounce(self, ball):
         #if the ball bounces off the paddle
         if self.x - self.width/2 < ball.x +ball.radius  and self.x + self.width/2 > ball.x - ball.radius:
             if ball.y - ball.vy + ball.radius <= self.y - self.height/2 <= ball.y + ball.radius:
                return ['tp']
        
         return []
            
points = [] 
class Brick:
    """creates brick"""
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self. color = color
        self.x = x
        self.y = y
        self.visible = True
        
        
    def draw(self):
        #draw the brick if the brick is visible
        if self.visible:            
            rect(self.x,self.y,self.width,self.height)
            fill(self.color[0], self.color[1], self.color[2])

        
    def bounce(self, ball):
        
        impact = []
        
        if self.visible:
            #if the brick is visible, the ball bounces off the brick
            if self.x - self.width/2 < ball.x +ball.radius  and self.x + self.width/2 > ball.x - ball.radius:
                if ball.y - ball.vy + ball.radius <= self.y - self.height/2 <= ball.y + ball.radius:
                    impact.append('t')
                if ball.y - ball.radius <= self.y + self.height/2 <= ball.y - ball.vy - ball.radius:
                    impact.append('b')
                
            if self.y - self.height/2 < ball.y + ball.radius and self.y + self.height/2 > ball.y - ball.radius:
                if ball.x - ball.vx + ball.radius <= self.x - self.width/2 <= ball.x + ball.radius:
                    impact.append('l')
                if ball.x - ball.radius <= self.x + self.width/2 <= ball.x - ball.vx - ball.radius:
                    impact.append('r')
                    
        if len(impact) > 0:
            #if the brick is hit, make the brick invisible and append an 'a' to the points list (points lists is to keep track of how many bricks are hit)
            self.visible = False
            points.append('a')
            
        return impact
        
        
class specialBrick:
    """hitting this brick changes the size of the ball"""
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self. color = color
        self.x = x
        self.y = y
        self.visible = True
        
    def draw(self):
        #draw the brick
        if self.visible:
            rect(self.x,self.y,self.width,self.height)
            fill(self.color[0], self.color[1], self.color[2])
            
    def bounce (self,ball):
        impact = []
        
        #if the brick is still visible, change the size of the brick
        if self.visible:
            if self.x - self.width/2 < ball.x +ball.radius  and self.x + self.width/2 > ball.x - ball.radius:
                if ball.y - ball.vy + ball.radius <= self.y - self.height/2 <= ball.y + ball.radius:
                    impact.append('f')
                if ball.y - ball.radius <= self.y + self.height/2 <= ball.y - ball.vy - ball.radius:
                    impact.append('g')
                
            if self.y - self.height/2 < ball.y + ball.radius and self.y + self.height/2 > ball.y - ball.radius:
                if ball.x - ball.vx + ball.radius <= self.x - self.width/2 <= ball.x + ball.radius:
                    impact.append('h')
                if ball.x - ball.radius <= self.x + self.width/2 <= ball.x - ball.vx - ball.radius:
                    impact.append('i')
                    
            
        
        if len(impact) > 0:                 #if the ball hits the brick, make the brick invisible
            self.visible = False
            
        return impact


obstacles = []

ball = Ball(WIDTH//2, HEIGHT//2, RADIUS, (0,0,255)) #creates the ball
paddle = Paddle(100,15, (0,0,0)) #creates the paddle


def setup(): #initializes everything (only run once)
    size(WIDTH, HEIGHT + 70)   #needs to be first line of setup, establishes us with window, dimentions of window we are creating
    noStroke()
    
    rectMode(CENTER)
        
    noCursor()
    
    #draw the normal bricks    
    for i in range (15):
        for j in range(20):
            brick = Brick(10 + j*30, 30 + i*15,30,10,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            obstacles.append(brick)   #append to obstacles list
            
   #draw the specialbrick        
    for i in range (15):
        for j in range (1,20,7):
            brick2 = specialBrick(10 + j*30, 30 + i*15,30,10,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            obstacles.append(brick2)   #append to obstacles list
               

obstacles.append(paddle)  #append the paddle to obstacles list


def draw():  #where we do all of our drawing; called from within a loop within pyprocessing
    background(255,255,255) #sets the background color
    paddle.update()         #updates the paddle
    ball.update(obstacles)  #updates the ball
    ball.draw()             #draws the ball

    

    for obstacle in obstacles:
    #draw all of the obstacles
        obstacle.draw()
   
            
    text('SCORE: ' + str(len(points)), WIDTH/2 - 90, HEIGHT + 50 )   #display the score
    textSize(30)
    if len(points) >= 300:                   #if you clear the board(maximum amount of points)                                  
        noLoop()                                #end the game
        cursor()                                #show cursor
        text('VICTORY!!!!', 200, HEIGHT/2 + 100) #display 'VICTORY!!!!' message
        

run()    #part of pyprocessing