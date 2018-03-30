from pygame.locals import *
from random import randint
import math
from math import hypot
import pygame
import time


grid = []
a = 0
for row in range(1,11):
    b = 0
    for col in range(1,11):
        grid.append([(row+a)*50,(col+b)*50])
        b += 1
    a += 1

class Target:
    x = 0
    y = 0
    step = 10

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Computer:
     x = 0
     y = 0
     step = 10
     direction = 0
     updateCountMax = 2
     gridMemory = []
     id = 0
     knownTargets = [ [ None for y in range( 5 ) ] for x in range( 5 ) ]



     def __init__(self):


         # initial positions, no collision.
         c = grid[randint(0,99)]
         self.x = c[0]
         self.y = c[1]

     def update(self):
         if self.direction == 0 and self.x < 950:
            self.x = self.x + self.step
         if self.direction == 1 and self.x > 50:
            self.x = self.x - self.step
         if self.direction == 2 and self.y > 50:
            self.y = self.y - self.step
         if self.direction == 3 and self.y < 950:
            self.y = self.y + self.step
         if [self.x,self.y] in grid:
             self.gridMemory.append([self.x,self.y])



     def moveRight(self):
         self.direction = 0

     def moveLeft(self):
         self.direction = 1

     def moveUp(self):
         self.direction = 2

     def moveDown(self):
         self.direction = 3

     def search(self):
         if [self.x,self.y] in grid:
             if self.x >= 150 and [self.x - self.step * 10, self.y] not in self.gridMemory:
                    self.moveLeft()

             elif self.y >= 150 and [self.x, self.y - self.step * 10] not in self.gridMemory:
                 for i in range(0, 10):
                    self.moveUp()

             elif self.x <= 850 and [self.x + self.step * 10, self.y] not in self.gridMemory:
                 for i in range(0, 10):
                    self.moveRight()

             elif self.y <= 850 and [self.x, self.y + self.step * 10] not in self.gridMemory:
                 for i in range(0, 10):
                    self.moveDown()
             else:
                 r = randint(0,3)
                 if r == 0 and self.x > 150:
                     self.moveLeft()
                 elif r == 1 and self.y > 150:
                     self.moveUp()
                 elif r == 2 and self.x < 850:
                     self.moveRight()
                 elif r == 3 and self.x < 850:
                     self.moveDown()



     def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Game:
    def isCollision(self, x1, y1, x2, y2):
        if math.hypot(x2-x1, y2-y1) <= 100:
            return True
        return False

class App:

    windowWidth = 1000
    windowHeight = 1000
    target = 0
    targets = [ [ None for y in range( 5 ) ] for x in range( 5 ) ]
    computer = []
    targetNum = [5,5,5,5,5]

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._agent_surf = None
        self._target_surf = None
        self.game = Game()
        for i in range(5):
            self.computer.append(Computer())
            for j in range(5):
                self.target = Target(randint(1, 99), randint(1, 99))
                self.targets[i][j]= self.target




    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        self._running = True
        self._agent_surf = pygame.image.load("agent.png").convert()
        self._agent_surf = pygame.transform.scale(self._agent_surf, (10,10))
        self._target_surf = pygame.image.load("target.png").convert()
        self._target_surf = pygame.transform.scale(self._target_surf, (10, 10))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):


        # does agent see target?
        for i in range(5):
            self.computer[i].search()
            self.computer[i].update()
            for j in range(5):
                if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[i].x, self.computer[i].y):
                    self.targets[i][j].x = -1000
                    self.targets[i][j].y = -1000
                    self.targetNum[i] -= 1
                    if self.targetNum[i] == 0:
                        self.on_render()
                        time.sleep(1)
                        self._running = False
                else:
                    for k in range(5):
                        if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[k].x, self.computer[k].y):
                            self.computer[k].knownTargets[i][j] = self.targets[i][j]
                            #print (self.computer[k].knownTargets[i][j])
                #if self.game.isCollision(self.computer[i].x, self.computer[i].y, self.computer[j].x, self.computer[j].y) and i != j:


    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        for i in range(5):
            self.computer[i].draw(self._display_surf, self._agent_surf)
            for j in range(5):
                self.targets[i][j].draw(self._display_surf, self._target_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self._running = False
            self.on_loop()


            self.on_render()

            time.sleep(50.0 / 1000.0);

        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()