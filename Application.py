import random
import time
from utilities import cmd
import keyboard
from threading import Thread
import sys
import re
import numpy as np
from playsound import playsound
import os

class GameManager:
    def __init__(self, map):
        self.instances = list()
        self.map = map
        self.former_bitmap = list()

    def Update(self):
        self.map.Draw()

class Amplifiers:
    def __init__(self):
        self.bomb_range = 2
        self.speed = 1


class Map:
    def __init__(self, rows, columns):
        self.bitmap = []
        self.rows = rows
        self.columns = columns
        self.icons = {'0':'  ', '1':'🔳', '2':'💥', '3':'🍄'}
        self.Initialize()
        self.LoadMap()

    def LoadMap(self):
        pass

    def Initialize(self):
        with open('Map.txt', 'r') as file:
            map = list()
            for line in file.readlines():
                map.append(line.split())

            for element in map:
                for x in element:
                    self.bitmap.append([self.icons[i] for i in x])

    def Draw(self):
        cmd.Window.clear()
        layout = ''
        for element in self.bitmap:
            for element in element:
                layout += element
            layout += '\n'
        print(layout, end='', flush=True)

class Bomb:
    def __init__(self, map, position: tuple, range: int):
        self.map = map
        self.bitmap = map.bitmap
        self.explosion = '💥'
        self.pos = position
        self.icon = ['💣', '🧨'][0]
        map.bitmap[position[0]][position[1]] = self.icon
        self.range = range
        Thread(target=self.Explode).start()

    def Update():
        while True:
            self.map.bitmap[position[0]][position[1]] = self.icon
            time.sleep(0.05)

    def Explode(self):
        time.sleep(1.5)
        self.DrawExplosion(self.range)
        #playsound('explosion.mp3')



    def DrawExplosion(self, r):
        pos = self.pos
        self.map.bitmap[self.pos[0]][self.pos[1]] = self.icon
        for i in range(pos[1] - r, pos[1] + r + 1):
            if not(i > 0 and i < 10):continue
            try:
                self.map.bitmap[pos[0]][i] = self.explosion
            except Exception:pass
        for i in range(pos[0] - r, pos[0] + r + 1):
            if not(i > 0 and i < 10):continue
            try:
                self.map.bitmap[i][pos[1]] = self.explosion
            except Exception:pass

        self.RemoveExplosion()
    def RemoveExplosion(self):
        time.sleep(0.25)
        for i, elem in enumerate(self.map.bitmap):
            for j, elem in enumerate(elem):
                if(elem == self.explosion):
                    self.map.bitmap[i][j] = '  '
    def __del__(self):
        pass

class AI:
    def __init__(self, map):
        self.health = 3
        self.icon = '🤖'
        self.position = (1, 1)
        self.bitmap = map.bitmap
        self.map = map

    def Update(self):
        if(self.health <= 0):return
        self.UpdateIcon()


    def UpdateIcon(self):
        self.Collision()
        self.bitmap[self.position[0]][self.position[1]] = self.icon

    def Collision(self):
        if(self.bitmap[self.position[0]][self.position[1]] == self.map.icons['2']):
            self.health -= 1

class Player(object):
    def __init__(self, map,gameManager, icon):
        self.powerups = Amplifiers()
        self.gm = gameManager
        self.velocity = (0, 1)
        self.health = 3
        self.map = map
        self.icon = icon
        self.pos = (9, 9)
        self.illegalMoves = [self.map.icons['1'], '💣']
        self.Initialize()

    def Initialize(self):
        self.map.bitmap[self.pos[0]][self.pos[1]] = self.icon
    def Move(self, direction):
        if(direction == 'None'):return
        self.RemoveIcon()
        if(input == 'left'):
            self.velocity = (0, -1)
            if self.Collision((0, -1)):
                self.pos = (self.pos[0], self.pos[1] - 1)

        elif(input == 'right'):
            self.velocity = (0, 1)
            if self.Collision((0, 1)):
                self.pos = (self.pos[0], self.pos[1] + 1)

        elif(input == 'up'):
            self.velocity = (-1, 0)
            if self.Collision((-1, 0)):
                self.pos = (self.pos[0] - 1, self.pos[1])

        elif(input == 'down'):
            self.velocity = (1, 0)
            if self.Collision((1, 0)):
                self.pos = (self.pos[0] + 1, self.pos[1])
        self.map.bitmap[self.pos[0]][self.pos[1]] = self.icon

    def Action(self, input: str):
        self.Update()
        if(input == 'space'):
            if(self.map.bitmap[self.pos[0] + self.velocity[0]][self.pos[1] + self.velocity[1]] not in self.illegalMoves):
                bomb = Bomb(self.map, (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]), self.powerups.bomb_range)
                self.gm.instances.append(bomb)
        else: self.Move(input)

    def Update(self):
        node = self.map.bitmap[self.pos[0]][self.pos[1]]
        if(node == '💥'):self.health -= 1
        node = self.icon
        print(self.health)

    def Collision(self, posDelta: tuple):
        position = (self.pos[0] + posDelta[0], self.pos[1] + posDelta[1])
        try:
            node = self.map.bitmap[position[0]][position[1]]
            if(node == '💣'):
                for elem in self.gm.instances:
                    if(elem.pos == position):
                        if(self.map.bitmap[elem.pos[0] + self.velocity[0]][elem.pos[1] + self.velocity[1]] != self.illegalMoves[0]):
                            self.map.bitmap[position[0]][position[1]] = '  '
                            elem.pos = (position[0] + self.velocity[0], position[1] + self.velocity[1])
                            self.map.bitmap[position[0] + self.velocity[0]][position[1] + self.velocity[1]] = '💣'
                            self.pos = position
            if(node == '🍄'):
                self.powerups.bomb_range += 1
                return True

            if(node not in self.illegalMoves):
                print(self.map.bitmap[position[0]][position[1]], flush=True)
                return True

        except IndexError: return True
        return False


    def RemoveIcon(self):
        self.map.bitmap[self.pos[0]][self.pos[1]] = '  '


input = ''
stop = False

def Main():
    Thread(target=Input).start()
    Thread(target=GameLoop).start()

def GameLoop():
    global input, stop
    map = Map(10, 10) # INITIALIZE OBJECTS
    gameManager = GameManager(map)
    player = Player(map, gameManager, '🤡')
    ai = AI(map)
    while not stop:
        gameManager.Update()
        player.Action(input)
        ai.Update()
        #cmd.Window.title(f"🤡 : {player.health}        🤖 : {ai.health}")
        input = 'None'
        time.sleep(0.005)

def Input():
    global input, stop
    while not stop:
        if(keyboard.is_pressed('w')):
            input = 'up'
        elif(keyboard.is_pressed('a')):
            input = 'left'
        elif(keyboard.is_pressed('s')):
            input = 'down'
        elif(keyboard.is_pressed('d')):
            input = 'right'
        elif(keyboard.is_pressed('q')):
            stop = True
        elif(keyboard.is_pressed('space')):
            input = 'space'
        time.sleep(0.2)

if __name__ == '__main__':
    Main()
