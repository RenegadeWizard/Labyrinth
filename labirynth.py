from datetime import datetime
from os import curdir, sep
from http.server import BaseHTTPRequestHandler,HTTPServer
from pip._vendor.distlib.compat import raw_input
import threading


class Labirynth:
    def __init__(self):
        """
        Preparing: create a maze etc"
        """
        self.matrix = [
            " #k   #   ###   ",
            " ####   #   # # ",
            "    ####### # # ",
            "# ###    ##   # ",
            "#     #### #### ",
            "##### #      #  ",
            "      ###### # #",
            " ######   ##   #",
            " #    # # ## # #",
            " # ## # #    #  ",
            " #### # ####### ",
            "  #   #       # ",
            "# # # # ### # # ",
            "  # # #   #   # ",
            " ## # ### # ### ",
            "    #     #@#   "
        ]
        self.charY=15
        self.charX=11
        self.isFinished=False
        self.upperRow=14
        self.start=datetime.now()

    def print(self):
        """Printing current state of a maze"""
        for i in range(len(self.matrix)):
            print(self.matrix[i])

    def print2lines(self):
        """Printing current state of 2 rows of a maze"""
        print(self.matrix[self.upperRow])
        print(self.matrix[self.upperRow+1])

    def playloop(self):
        """Loop for play with full maze"""
        while (self.isFinished==False):
            self.print()
            direction=raw_input().split()[0]
            self.move(direction)
            print(" ")
            print(" ")
        return (datetime.now()-self.start)

    def play2rows(self):
        """Loop for play with 2 rows"""
        while (self.isFinished==False):
            self.print2lines()
            direction=raw_input().split()[0]
            self.move(direction)
            print(" ")
            print(" ")
        return (datetime.now() - self.start)

    def move (self, site):
        """Changing state of a play by a player"""
        if (site=='u'): #up
            if (self.charY>0 and self.matrix[self.charY-1][self.charX]!='#'):
                if  self.matrix[self.charY-1][self.charX]=='k':
                    self.isFinished=True
                localVar=list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                self.matrix[self.charY]="".join(localVar)
                localVar=list(self.matrix[self.charY - 1])
                localVar[self.charX]='@'
                self.matrix[self.charY-1]="".join(localVar)
                self.charY-=1
        if (site=='d'): #down
            if (self.charY<15 and self.matrix[self.charY+1][self.charX]!='#'):
                if  self.matrix[self.charY+1][self.charX]=='k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                self.matrix[self.charY] = "".join(localVar)
                localVar = list(self.matrix[self.charY + 1])
                localVar[self.charX] = '@'
                self.matrix[self.charY + 1] = "".join(localVar)
                self.charY+=1
        if (site=='l'): #left
            if (self.charX>0 and self.matrix[self.charY][self.charX-1]!='#'):
                if  self.matrix[self.charY][self.charX-1]=='#k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                localVar[self.charX-1] = '@'
                self.matrix[self.charY] = "".join(localVar)
                self.charX-=1
        if (site=='r'): #right
            if (self.charX<15 and self.matrix[self.charY][self.charX+1]!='#'):
                if  self.matrix[self.charY][self.charX+1]=='#k':
                    self.isFinished=True
                localVar = list(self.matrix[self.charY])
                localVar[self.charX] = ' '
                localVar[self.charX+1] = '@'
                self.matrix[self.charY] = "".join(localVar)
                self.charX+=1
        if (site=='c'): #cheating
            self.isFinished=True
        if (site=='w'): #show row up
            if (self.upperRow>0):
                self.upperRow-=1
        if (site == 's'):  # show row down
            if (self.upperRow <14):
                self.upperRow += 1

class Ranking:
    def reloadRanking(self, result):
        """Reloading ranking after end of a game"""
        file = open("wyniki.txt", "r")
        results = []
        for i in range(10):
            res = file.readline()
            results.append(res)
        file.close()
        results.append(result)
        results.sort()
        print("Best results are:")
        file = open("wyniki.txt", "w")
        for i in range(10):
            print(i, results[i])
            file.write(results[i])
            file.write("\n")
        file.close()

    def returnCurrentRankingFileAsString(self):
        """Reading current version of ranking and returning it as string
        (will be used to serve ranking in a browser)"""
        file=open("wyniki.txt","r")
        fullFile=""
        for i in range(10):
            fullFile += file.readline()
        file.close()
        return fullFile


class localStaff(threading.Thread):
    def __init__(self, ranking):
        self.rank=ranking

    def run(self):
        lab = Labirynth()
        result = lab.playloop()
        print("Your result is", result)
        self.ranking.reloadRanking(result)


class serverStaff(threading.Thread):
    def __init__(self,ranking):
        self.rank=ranking

    def run(self):
        pass

if __name__=="__main__":
    rank=Ranking()
    localStaff(rank).run()
    serverStaff(rank).run()



