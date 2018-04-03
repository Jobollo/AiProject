from __future__ import division
from pygame.locals import *
from random import randint
import math
from math import hypot
import pygame
import time
import csv
import numpy as np

#agents move along this grid and remember which points they'vr been to
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
     #this is how fast agents move
     step = 10
     updateCountMax = 2



     def __init__(self):
         self.direction = 0
         #memory of where the agent has been on the grid
         self.gridMemory = []
         #holds location of targets that didn't belong to them
         self.knownTargets = [[[None for z in range(2)] for y in range(5)] for x in range(5)]
         #coordinates of a target that another agent told them
         self.nextTarget = []
         #if 0 it means they don't know where their next target is but if 1 they have been told the location
         #of one of their targets
         self.knowsTarget = 0
         #previous x and y
         self.steps = 0
         self.prevX = 0
         self.prevY = 0
         self.empathy = 0
         self.memory = [0,0,0,0,0]
         self.chanceToHelp = 0
         # initial positions, no collision.
         c = grid[randint(0,99)]
         self.x = c[0]
         self.y = c[1]

     #updates location of agent based on the direction they're moving
     def update(self):
         self.prevX = self.x
         self.prevY = self.y
         if self.direction == 0 and self.x < 950:
            self.x = self.x + self.step
            self.steps += 1
         if self.direction == 1 and self.x > 50:
            self.x = self.x - self.step
            self.steps += 1
         if self.direction == 2 and self.y > 50:
            self.y = self.y - self.step
            self.steps += 1
         if self.direction == 3 and self.y < 950:
            self.y = self.y + self.step
            self.steps += 1
         #if the point they are on is in the grid then add it to the memory
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
         #only able to change direction if they are on a grid point
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
             #if they have been to every point around them and they are stuck, choose a random direction
             else:
                 r = randint(0,3)
                 if r == 0 and self.x > 150:
                     self.moveLeft()
                 elif r == 1 and self.y > 150:
                     self.moveUp()
                 elif r == 2 and self.x < 850:
                     self.moveRight()
                 elif r == 3 and self.y < 850:
                     self.moveDown()
         #sometimes they get stuck on a point that is not on the grid when they use the moveToTarget function
         #so this will get them unstuck if that happens
         if self.x == self.prevX and self.y == self.prevY:
             if self.x > 50:
                 self.moveLeft()
             elif self.x < 950:
                 self.moveRight()
             elif self.y > 50:
                 self.moveUp()
             elif self.y < 950:
                 self.moveDown()

     #this function is used when an agent knows the location of one of their targets
     def moveToTarget(self, x,y):
         if self.x > x:
             self.moveLeft()

         if self.x < x:
             self.moveRight()

         if self.x == x:
             if self.y < y:
                 self.moveDown()

             if self.y > y:
                 self.moveUp()



     def draw(self, surface, image):
         surface.blit(image, (self.x, self.y))



     def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

class Game:
    #checks if the 2 coordinates inputted are within 100 pixels of eachother which is the range of the agent's radar
    def isCollision(self, x1, y1, x2, y2):
        if math.hypot(x2-x1, y2-y1) <= 100:
            return True
        return False

class App:

    windowWidth = 1000
    windowHeight = 1000


    def __init__(self):
        self.target = 0
        # list of all targets
        self.targets = [[None for y in range(5)] for x in range(5)]
        self.computer = []
        # list of targets left for each agent
        self.targetNum = [5, 5, 5, 5, 5]
        self.scenario = 0
        self.steps = [0,0,0,0,0]
        self._running = True
        self._display_surf = None
        self._agent_surf = []
        self._target_surf = []
        self.agentModels = ["agent0.png","agent1.jpg","agent2.jpg","agent3.jpg","agent4.jpg"]
        self.game = Game()
        for i in range(5):
            #list of agents
            self.computer.append(Computer())
            for j in range(5):
                #assigning random coordinates to targets
                self.target = Target(randint(1, 99), randint(1, 99))
                self.targets[i][j]= self.target




    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        self._running = True
        for i in range(5):
            self._agent_surf.append(pygame.image.load(self.agentModels[i]).convert())
            self._agent_surf[i] = pygame.transform.scale(self._agent_surf[i], (15, 15))
            self._target_surf.append(pygame.image.load(self.agentModels[i]).convert())
            self._target_surf[i] = pygame.transform.scale(self._target_surf[i], (10, 10))

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    #first scenario
    def competition(self):
        self.scenario = 1
        for i in range(5):
            self.computer[i].search()
            self.computer[i].update()
            self.steps[i] = self.computer[i].steps
            for j in range(5):
                #agent finds one of its targets so target disappears
                if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[i].x, self.computer[i].y):
                    self.targets[i][j].x = -1000
                    self.targets[i][j].y = -1000
                    self.targetNum[i] -= 1
                    #if agent has no targets left end game
                    if self.targetNum[i] == 0:
                        print "agent " + str(i) + " wins."
                        self.on_render()
                        time.sleep(1)
                        self._running = False
                else:
                    for k in range(5):
                        if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[k].x, self.computer[k].y):
                            self.computer[k].knownTargets[i][j] = self.targets[i][j]

    #second scenario
    def collaboration(self):
        self.scenario = 2
        for i in range(5):
            #agent doesn't know target so continue searching
            if self.computer[i].knowsTarget == 0:
                self.computer[i].search()
            #agent knows where a target is so go to it
            elif self.computer[i].knowsTarget == 1:
                self.computer[i].moveToTarget(self.computer[i].nextTarget[0],self.computer[i].nextTarget[1])
            self.computer[i].update()
            self.steps[i] = self.computer[i].steps
            for j in range(5):
                if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[i].x, self.computer[i].y):
                    self.targets[i][j].x = -1000
                    self.targets[i][j].y = -1000
                    #targets that are found are removed from all agents known target memory so that they don't tell
                    #another agent about a target that isn't there
                    for k in range(5):
                        self.computer[k].knownTargets[i][j] = [None, None]
                    #if an agent just found a target that another agent told them about then the agent might not
                    #be on the grid anymore and would get stuck so this puts them back on the grid in that scenario
                    if self.computer[i].knowsTarget == 1:
                       if all(self.computer[i].x not in el for el in grid):
                           if self.computer[i].x < 950:
                                self.computer[i].moveRight()
                           else:
                                self.computer[i].moveLeft()
                       if all(self.computer[i].y not in el for el in grid):
                           if self.computer[i].y > 50:
                                self.computer[i].moveUp()
                           else:
                                self.computer[i].moveDown()
                    #set knows target back to 0 so that search continues
                    self.computer[i].knowsTarget = 0
                    self.targetNum[i] -= 1
                    #game ends when all agents have collected all of their targets
                    if all(el == 0 for el in self.targetNum):
                        self.on_render()
                        time.sleep(1)
                        self._running = False
                else:
                    #if an agent collides with a target that isn't theirs then they will remember where they were
                    #when they collided with it so that they can tell whoever it belonged to
                    for k in range(5):
                        if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[k].x, self.computer[k].y):
                            self.computer[k].knownTargets[i][j][0] = self.computer[k].x
                            self.computer[k].knownTargets[i][j][1] = self.computer[k].y
                #if 2 agents collide then they chack if they have any targets that belong to the other agent and then they tell them
                if  i != j and self.game.isCollision(self.computer[i].x, self.computer[i].y, self.computer[j].x, self.computer[j].y):
                    if self.computer[j].knowsTarget != 1 and next(item for item in self.computer[i].knownTargets[j] if item is not None) != [None, None]:
                        print "agent " + str(i) + " helped agent " + str(j) + "."
                        self.computer[j].knowsTarget = 1
                        try:
                            self.computer[j].nextTarget = next(item for item in self.computer[i].knownTargets[j] if item is not None)
                        except Exception as e:
                            print e
                    if self.computer[i].knowsTarget != 1 and next(item for item in self.computer[j].knownTargets[i] if item is not None) != [None, None]:
                        print "agent " + str(j) + " helped agent " + str(i) + "."
                        self.computer[i].knowsTarget = 1
                        try:
                            self.computer[i].nextTarget = next(item for item in self.computer[j].knownTargets[i] if item is not None)
                        except Exception as e:
                            print e
    #third scenario
    def compassion(self):
        self.scenario = 3
        for i in range(5):
            if self.computer[i].knowsTarget == 0:
                self.computer[i].search()
            elif self.computer[i].knowsTarget == 1:
                self.computer[i].moveToTarget(self.computer[i].nextTarget[0],self.computer[i].nextTarget[1])
            self.computer[i].update()
            self.steps[i] = self.computer[i].steps
            for j in range(5):
                if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[i].x, self.computer[i].y):
                    self.targets[i][j].x = -1000
                    self.targets[i][j].y = -1000
                    #empathy increasing will make it more likely this agent will help an agent who has
                    #collected less targets
                    self.computer[i].empathy += 20
                    for k in range(5):
                        self.computer[k].knownTargets[i][j] = [None, None]
                    if self.computer[i].knowsTarget == 1:
                       if all(self.computer[i].x not in el for el in grid):
                           if self.computer[i].x < 950:
                                self.computer[i].moveRight()
                           else:
                                self.computer[i].moveLeft()
                       if all(self.computer[i].y not in el for el in grid):
                           if self.computer[i].y > 50:
                                self.computer[i].moveUp()
                           else:
                                self.computer[i].moveDown()
                    self.computer[i].knowsTarget = 0
                    self.targetNum[i] -= 1
                    if self.targetNum[i] == 0:
                        print "agent " + str(i) + " wins."
                        self.on_render()
                        time.sleep(1)
                        self._running = False
                else:
                    for k in range(5):
                        if self.game.isCollision(self.targets[i][j].x, self.targets[i][j].y, self.computer[k].x, self.computer[k].y):
                            self.computer[k].knownTargets[i][j][0] = self.computer[k].x
                            self.computer[k].knownTargets[i][j][1] = self.computer[k].y
                if  i != j and self.game.isCollision(self.computer[i].x, self.computer[i].y, self.computer[j].x, self.computer[j].y):
                    if self.computer[j].knowsTarget != 1 and next(item for item in self.computer[i].knownTargets[j] if item is not None) != [None, None]:
                        #chance to help is calculated based on how many targets each agent has collected and also
                        #if the agent they might help has helped them before
                        self.computer[i].chanceToHelp = self.computer[i].empathy - self.computer[j].empathy + self.computer[i].memory[j]
                        r = randint(0, 100)
                        if r < self.computer[i].chanceToHelp:
                            print "agent " + str(i) + " helped agent " + str(j) + "."
                            self.computer[j].knowsTarget = 1
                            try:
                                self.computer[j].nextTarget = next(item for item in self.computer[i].knownTargets[j] if item is not None)
                                self.computer[j].memory[i] += 10
                            except Exception as e:
                                print e
                        else:
                            print "agent " + str(i) + " didn't want to help agent " + str(j) + "."
                    if self.computer[i].knowsTarget != 1 and next(item for item in self.computer[j].knownTargets[i] if item is not None) != [None, None]:
                        self.computer[j].chanceToHelp = self.computer[j].empathy - self.computer[i].empathy + self.computer[j].memory[i]
                        r = randint(0, 100)
                        if r < self.computer[j].chanceToHelp:
                            print "agent " + str(j) + " helped agent " + str(i) + "."
                            self.computer[i].knowsTarget = 1
                            try:
                                self.computer[i].nextTarget = next(item for item in self.computer[j].knownTargets[i] if item is not None)
                                self.computer[i].memory[j] += 10
                            except Exception as e:
                                print e
                        else:
                            print "agent " + str(j) + " didn't want to help agent " + str(i) + "."


    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        for i in range(5):
            self.computer[i].draw(self._display_surf, self._agent_surf[i])
            for j in range(5):
                self.targets[i][j].draw(self._display_surf, self._target_surf[i])
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self, scen):
        if self.on_init() is False:
            self._running = False
        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self._running = False
            if scen == 1:
                self.competition()

            if scen == 2:
                self.collaboration()
            if scen == 3:
                self.compassion()


            self.on_render()

            time.sleep(50.0 / 1000.0);

        self.on_cleanup()


if __name__ == "__main__" :
    csv = open("G27_1.csv", "w")
    csv2 = open("G27_2.csv", "w")
    columnTitleRow = "Scenario number, Iteration number, Agent number, # of targets collected, # of steps, " \
                     "Agent happiness, Max happiness, Min happiness, Average happiness, Standard deviation of " \
                     "happiness, Agent competitivness\n"
    columnTitleRow2 = "Scenario number, Average happiness, Agent competitivness\n"
    csv.write(columnTitleRow)
    csv2.write(columnTitleRow2)
    c = [1,2,3,4,5]
    print "agent 0 = blue"
    print "agent 1 = green"
    print "agent 2 = orange"
    print "agent 3 = purple"
    print "agent 4 = brown"

    iarr = []
    karr = []
    for l in range(10):
        theApp = App()
        theApp.on_execute(1)
        a = theApp.scenario
        b = l + 1
        d = []
        e = []
        f = []
        for m in range(5):
            d.append(5 - theApp.targetNum[m])
            e.append(theApp.steps[m])
            f.append(d[m]/(e[m]+1))
        print f
        g = max(f)
        h = min(f)
        arr = np.array(f)
        i = np.mean(arr)
        iarr.append(i)
        j = np.std(arr)
        for m in range(5):
            k = (f[m] - h) / (g - h)
            karr.append(k)
            row = (str(a) + "," + str(b) + "," + str(c[m]) + "," + str(d[m]) + "," + str(e[m]) + "," + str(f[m])
                   + "," + str(g) + "," + str(h) + "," + str(i) + "," + str(j) + "," + str(k)) + "\n"
            csv.write(row)
    row = (str(a) + "," + str(np.mean(iarr)) + "," + str(np.mean(karr))) + "\n"
    csv2.write(row)

    iarr = []
    karr = []
    for l in range(10):
        theApp = App()
        theApp.on_execute(2)
        a = theApp.scenario
        b = l + 1
        d = []
        e = []
        f = []
        for m in range(5):
            d.append(5 - theApp.targetNum[m])
            e.append(theApp.steps[m])
            f.append(d[m]/(e[m]+1))
        print f
        g = max(f)
        h = min(f)
        arr = np.array(f)
        i = np.mean(arr)
        iarr.append(i)
        j = np.std(arr)
        for m in range(5):
            k = 0
            karr.append(k)
            row = (str(a) + "," + str(b) + "," + str(c[m]) + "," + str(d[m]) + "," + str(e[m]) + "," + str(f[m])
                   + "," + str(g) + "," + str(h) + "," + str(i) + "," + str(j) + "," + str(k)) + "\n"
            csv.write(row)
    row = (str(a) + "," + str(np.mean(iarr)) + "," + str(np.mean(karr))) + "\n"
    csv2.write(row)

    iarr = []
    karr = []
    for l in range(10):
        theApp = App()
        theApp.on_execute(3)
        a = theApp.scenario
        b = l + 1
        d = []
        e = []
        f = []
        for m in range(5):
            d.append(5 - theApp.targetNum[m])
            e.append(theApp.steps[m])
            f.append(d[m]/(e[m]+1))
        print f
        g = max(f)
        h = min(f)
        arr = np.array(f)
        i = np.mean(arr)
        iarr.append(i)
        j = np.std(arr)
        for m in range(5):
            k = (f[m] - h) / (g - h)
            karr.append(k)
            row = (str(a) + "," + str(b) + "," + str(c[m]) + "," + str(d[m]) + "," + str(e[m]) + "," + str(f[m])
                   + "," + str(g) + "," + str(h) + "," + str(i) + "," + str(j) + "," + str(k)) + "\n"
            csv.write(row)
    row = (str(a) + "," + str(np.mean(iarr)) + "," + str(np.mean(karr))) + "\n"
    csv2.write(row)

