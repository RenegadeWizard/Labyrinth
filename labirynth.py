from datetime import datetime

from pip._vendor.distlib.compat import raw_input


class Labirynth:
    def __init__(self):
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
        for i in range(len(self.matrix)):
            print(self.matrix[i])

    def print2lines(self):
        print(self.matrix[self.upperRow])
        print(self.matrix[self.upperRow+1])

    def playloop(self):
        while (self.isFinished==False):
            self.print()
            direction=raw_input().split()[0]
            self.move(direction)
            print(" ")
            print(" ")
        return (datetime.now()-self.start)

    def play2rows(self):
        while (self.isFinished==False):
            self.print2lines()
            direction=raw_input().split()[0]
            self.move(direction)
            print(" ")
            print(" ")
        return (datetime.now() - self.start)

    def move (self, site):
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

if __name__=="__main__":
    lab=Labirynth()
    print(lab.play2rows())