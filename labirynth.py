#!/usr/bin/env python3
from datetime import datetime
from time import sleep
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import lcd
import keyboard
import sqlite3
import socket

UP = ['2']
DOWN = ['5', '8']
RIGHT = ['6']
LEFT = ['4']
ENTER = '*'


class MainScreen:
    def __init__(self, my_lcd, my_keyboard):
        self.my_lcd = my_lcd
        self.my_keyboard = my_keyboard
        self.which = 1
        self.my_lcd.show(self.which)

    def choose(self):
        key = ''
        while key != ENTER:
            key = self.my_keyboard.check()
            if key == '#':
                self.settings()
            if key in LEFT and self.which > 1:
                self.which -= 1
            if key in RIGHT and self.which < 5:
                self.which += 1
            self.my_lcd.show(self.which)
        return self.which

    def settings(self):
        key = ''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        self.my_lcd.settings(ip, "1234")
        while key != '#':
            key = self.my_keyboard.check()
        self.my_lcd.clear()
        self.my_lcd.show(self.which)

    def end(self):
        self.my_lcd.end()

labs =    [["###k############",
            "###            #",
            "#########   ####",
            "##             #",
            "##  ############",
            "#            ###",
            "#### ###########",
            "#### ###    ####",
            "#### ### #######",
            "####      ######",
            "#### ###########",
            "#### ###    ####",
            "####     #######",
            "##### ##########",
            "###         ####",
            "#########@######"],

           ["#######k########",
            "##      ########",
            "### ###     ####",
            "### ### ### ####",
            "### ### ## #####",
            "# #          ###",
            "# # ############",
            "# #           ##",
            "# ########## ###",
            "# ##   ### # ###",
            "# ## ##### # ###",
            "#          # ###",
            "#### ### ### ###",
            "#### ###     ###",
            "#### ###########",
            "####@###########"],

           ["####k###########",
            "#### ##      ###",
            "#### ## ########",
            "#### ## ########",
            "####          ##",
            "############# ##",
            "#         ### ##",
            "# #######     ##",
            "#    ###########",
            "#### # #########",
            "#### # ##     ##",
            "#### #    ### ##",
            "#### #### ### ##",
            "#### #### ### ##",
            "####          ##",
            "#########@######"],

           ["#####k##########",
            "##### ##########",
            "# #       ## ###",
            "# # # ### ## ###",
            "#   # #   ##  ##",
            "##### # ##### ##",
            "##### # ####  ##",
            "      # ###  ###",
            "######      ####",
            "#     ####  ####",
            "# ## #  # #    #",
            "# ## ##   # #  #",
            "# ##  ## ##  # #",
            "## ##    ##### #",
            "## ## ##       #",
            "#@    ##########"],

           ["##############k#",
            "######### #### #",
            "#    ## # #### #",
            "# ## ## #      #",
            "# ## ## # #### #",
            "# ## ## # #### #",
            "# ## ## # #### #",
            "####    # #### #",
            "#### #### ##   #",
            "#### #### ## ###",
            "##        ## ###",
            "## ######    ###",
            "## ####### ### #",
            "##      ## ### #",
            "####### ##     #",
            "#######@########"]]


class Labirynth:
    def __init__(self, myLcd, my_keyboard, which):
        """
        Preparing: create a maze etc"
        """
        self.matrix = labs[which-1]
        self.myLcd = myLcd
        self.my_keyboard = my_keyboard
        self.charY = 15
        self.charX = self.matrix[-1].index('@')
        self.isFinished = False
        self.upperRow = 14
        self.start = datetime.now()
        self.which = which

    def print(self):
        """Printing current state of a maze"""
        for i in range(len(self.matrix)):
            print(self.matrix[i])

    def print_lcd(self):
        if self.charY >= 14:
            self.myLcd.show(self.matrix[-4:])
        elif self.charY == 13:
            self.myLcd.show(self.matrix[-5:-1])
        elif self.charY < 3:
            self.myLcd.show(self.matrix[:4])
        else:
            self.myLcd.show(self.matrix[self.charY-2:self.charY-13])

    def print2lines(self):
        """Printing current state of 2 rows of a maze"""
        print(self.matrix[self.upperRow])
        print(self.matrix[self.upperRow+1])

    def playloop(self):
        """Loop for play with full maze"""
        while not self.isFinished:
            self.print_lcd()
            direction = self.my_keyboard.check()
            self.move(direction)
        return datetime.now()-self.start

    def play2rows(self):
        """Loop for play with 2 rows"""
        while not self.isFinished:
            self.print2lines()
            # direction = raw_input().split()[0]
            self.move(direction)
            print(" ")
            print(" ")
        return datetime.now() - self.start

    def move(self, site):
        """Changing state of a play by a player"""
        if site in UP:  # up
            if self.charY > 0 and self.matrix[self.charY-1][self.charX] != '#':
                if self.matrix[self.charY-1][self.charX] == 'k':
                    self.isFinished = True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                self.matrix[self.charY] = "".join(localVar)
                localVar = list(self.matrix[self.charY - 1])
                localVar[self.charX] = '@'
                self.matrix[self.charY-1] = "".join(localVar)
                self.charY -= 1
        if site in DOWN:    # down
            if self.charY < 15 and self.matrix[self.charY+1][self.charX] != '#':
                if self.matrix[self.charY+1][self.charX] == 'k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                self.matrix[self.charY] = "".join(localVar)
                localVar = list(self.matrix[self.charY + 1])
                localVar[self.charX] = '@'
                self.matrix[self.charY + 1] = "".join(localVar)
                self.charY += 1
        if site in LEFT:    # left
            if self.charX > 0 and self.matrix[self.charY][self.charX-1] != '#':
                if self.matrix[self.charY][self.charX-1] == 'k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                localVar[self.charX-1] = '@'
                self.matrix[self.charY] = "".join(localVar)
                self.charX -= 1
        if site in RIGHT:   # right
            if self.charX < 15 and self.matrix[self.charY][self.charX+1] != '#':
                if self.matrix[self.charY][self.charX+1] == 'k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                localVar[self.charX+1] = '@'
                self.matrix[self.charY] = "".join(localVar)
                self.charX += 1
        if site == 'c':   # cheating
            self.isFinished = True
        if site == 'w':  # show row up
            if self.upperRow > 0:
                self.upperRow -= 1
        if site == 's':  # show row down
            if self.upperRow < 14:
                self.upperRow += 1


class Ranking:
    def __init__(self, data_base):
        self.conn = sqlite3.connect(data_base)

    def reloadRanking(self, result):
        """Reloading ranking after end of a game"""
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO results(nick, result) VALUES(?, ?)''', result)
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def returnCurrentRankingFileAsString(self):
        """Reading current version of ranking and returning it as string
        (will be used to serve ranking in a browser)"""
        file = open("wyniki.txt", "r")
        fullFile = ""
        for i in range(10):
            fullFile += file.readline()
        file.close()
        return fullFile


class localStaff:
    """Class for local work (game)"""
    def __init__(self, ranking, myLcd, myKeyboard, which):
        self.rank = ranking
        self.myLcd = myLcd
        self.myKeyboard = myKeyboard
        self.which = which

    def run(self):
        lab = Labirynth(self.myLcd, self.myKeyboard, self.which)
        result = lab.playloop()
        result = result.seconds
        self.myLcd.win(result)
        key = self.myKeyboard.check()
        nick = ''
        while key != '*':
            key = self.myKeyboard.check()
            if key != '' and key != '*':
                self.myLcd.nick(key)
                nick += key
            sleep(0.3)
        self.rank.reloadRanking((nick, result))


if __name__ == "__main__":
    while True:
        rank = Ranking("dane.db")
        my_keyboard = keyboard.Keyboard()
        main_screen = MainScreen(lcd.LcdMainScreen(), my_keyboard)
        which = main_screen.choose()
        mylcd = lcd.Lcd()
        localStaff(rank, mylcd, my_keyboard, which).run()
        main_screen.end()
        while my_keyboard.check() != ENTER:
            pass
