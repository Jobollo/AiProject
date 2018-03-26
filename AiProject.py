from pygame.locals import *
from random import randint
import math
from math import hypot
import pygame
import time

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
     a = 0
     step = 10
     direction = 0
     updateCountMax = 2
     pointMemory = [[-1,-1]]

     def __init__(self):


         # initial positions, no collision.
         self.x = randint(1,99) * 10
         self.y = randint(1,99) * 10

     def update(self):
         if self.a <= 4:
             for i in range(0,len(self.pointMemory)):
                 if self.direction == 0 and self.x + self.step == self.pointMemory[i][0] and self.y == self.pointMemory[i][1]:
                     return
                 if self.direction == 1 and self.x - self.step == self.pointMemory[i][0] and self.y == self.pointMemory[i][1]:
                     return
                 if self.direction == 2 and self.y - self.step == self.pointMemory[i][1] and self.x == self.pointMemory[i][0]:
                     return
                 if self.direction == 3 and self.y + self.step == self.pointMemory[i][1] and self.x == self.pointMemory[i][0]:
                     return
         if self.direction == 0:
             self.x = self.x + self.step
         if self.direction == 1:
             self.x = self.x - self.step
         if self.direction == 2:
             self.y = self.y - self.step
         if self.direction == 3:
             self.y = self.y + self.step
         self.pointMemory.append([self.x,self.y])
         self.a = 0


     def moveRight(self):
         self.direction = 0

     def moveLeft(self):
         self.direction = 1

     def moveUp(self):
         self.direction = 2

     def moveDown(self):
         self.direction = 3

     def search(self):
         if self.x > 0 and self.direction != 0:
             self.moveLeft()

         elif self.y > 0 and self.direction != 3:
            self.moveUp()

         elif self.x < 990:
             self.moveRight()

         elif self.y < 990:
             self.moveDown()

         self.a += 1


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

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._agent_surf = None
        self._target_surf = None
        self.game = Game()
        self.target = Target(randint(1,99), randint(1,99))
        self.computer = Computer()

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
        self.computer.search()
        self.computer.update()

        # does agent see target?
        if self.game.isCollision(self.target.x, self.target.y, self.computer.x, self.computer.y):
            self.target.x = randint(1, 99) * 10
            self.target.y = randint(1, 99) * 10


        pass

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.target.draw(self._display_surf, self._target_surf)
        self.computer.draw(self._display_surf, self._agent_surf)
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