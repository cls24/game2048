import math,random
import sys,time,os
import re, sys, time, os
from ctypes import Structure, c_short, windll, byref
from shutil import get_terminal_size
from pynput.keyboard import Listener

"""
18888988886
7    7    7
288881188884
7    7    7
388881088885
"""
class GridMatrix():
    cmap = " ,┌,├,└,┤,┘,┐,│,─,┬,┴,┼".split(",")
    def __init__(self,row):
        self.row = row
        self.numMatrix=self.initMatrix()

    def initMatrix(self):
        maxN = self.row -1
        tmp = [[0]*self.row for i in range(self.row)]
        x, y = random.randint(0, maxN), random.randint(0, maxN)
        tmp[x][y] = 2
        while True:
            nx,ny = random.randint(0, maxN), random.randint(0, maxN)
            if x != nx and y!=ny:
                tmp[nx][ny] = random.choice([4]+[2]*9)
                break
        return tmp

    def makeNumRow(self,c):
        tmp=[]
        numList = self.numMatrix[c]
        c = 0
        for i in range(self.row*2+1):
            if i%2==0:
                tmp.append("│")
            else:
                tmp.append(str(numList[c]).rjust(4))
                c+=1
        return tmp

    def makeBorderRow(self,f,m,l):
        tmp=[]
        for i in range(self.row*2+1):
            if i==0:
                tmp.append(f)
            elif i%2 !=0:
                tmp += [8] * 4
            elif i==self.row*2:
                tmp.append(l)
            else:
                tmp.append(m)
        return tmp

    def makeMatrix(self):
        l=[]
        c= 0
        for i in range(self.row*2+1):
            if i%2!=0:
                tmp=self.makeNumRow(c)
                c += 1
            elif i==0:
                tmp=self.makeBorderRow(1,9,6)
            elif i==self.row*2:
                tmp=self.makeBorderRow(3,10,5)
            else:
                tmp = self.makeBorderRow(2, 11, 4)
            l.append(tmp)
        return l

    def genRandomNum(self):
        maxIdx = 11
        num = int(math.pow(2, random.randint(1, 11)))
        return str(num).rjust(4)



    def genGridStr(self):
        tmp=[]
        def zero(x):
            return  " "*4 if x=='   0' else x
        for i,v in enumerate(self.makeMatrix()):
            if i%2==0:
                tmp.append("".join([self.cmap[j] for j in v])+"\n")
            else:
                tmp.append("".join(map(lambda x:zero(x),v))+"\n")
        return "".join(tmp)


class Move():
    def __init__(self,matrix):
        self.matrix = matrix

    def genNumInZeros(self):
        n = random.choice([4]+[2]*9)
        tmp = []
        for x,row in enumerate(self.matrix):
            for y,num in enumerate(row):
                if num == 0:
                    tmp.append((x,y))
        aix = random.choice(tmp)
        self.matrix[aix[0]][aix[1]]=n

    def add(self,l):
        tmp = [i for i in l if i!=0]
        l=[]
        i=0
        while i<len(tmp)-1:
            if tmp[i] == tmp[i + 1]:
                l.append(tmp[i] + tmp[i + 1])
                i+=1
            else:
                l.append(tmp[i])
            i+=1
        if i==len(tmp)-1:
            l.append(tmp[i])
        l+=[0]*(4-len(tmp))
        return  l

    def reverse(self):
        for i in range(len(self.matrix)):
            self.matrix[i].reverse()

    def reshape(self):
        l = []
        for i in range(len(self.matrix)):
            l.append([self.matrix[j][i] for j in range(len(self.matrix))])
        self.matrix = l

    def move(self,way):
        lastMatrix = self.matrix
        if way=="a":
            self.matrix=self.left()
        elif way == "d":
            self.reverse()
            self.matrix = self.left()
            self.reverse()
        elif way == "w":
            self.reshape()
            self.matrix = self.left()
            self.reshape()
        elif way == "s":
            self.reshape()
            self.reverse()
            self.matrix = self.left()
            self.reverse()
            self.reshape()
        if self.matrix != lastMatrix:
            self.genNumInZeros()
    def left(self):
        tmp=[]
        for i in self.matrix:
            l = self.add(i)
            if len(l) !=4:
                l+=[0]*(4-len(l))
            tmp.append(l)
        return tmp


class OptMatrix():
    def __init__(self):
        self.grid = GridMatrix(4)
        self.move = Move(self.grid.numMatrix)
        # self.matrix = self.grid.numMatrix

    def listen(self):
        with Listener(on_press=self.show) as listener:
            listener.join()

    def show(self,key):
        class Pos(Structure):
            _fields_ = [('X', c_short), ('Y', c_short)]

        class Rect(Structure):
            _fields_ = [('Left', c_short), ('Top', c_short), ('Right', c_short), ('Bottom', c_short)]

        class Screen(Structure):
            _fields_ = [('Size', Pos), ('CursorPosition', Pos), ('Attributes', c_short), ('Window', Rect),
                        ('MaximumWindowSize', Pos)]

        h = windll.kernel32.GetStdHandle(-11)
        s = Screen()
        windll.kernel32.GetConsoleScreenBufferInfo(h, byref(s))
        current_position = s.CursorPosition

        ways = ["w", "d", "s", "a"]
        # g = GridMatrix(4)
        # move = Move(g.makeMatrix())
        try:
            way = key.char
            if way in ways:
                self.move.move(way)
                self.grid.numMatrix = self.move.matrix
                print(self.grid.genGridStr())
                windll.kernel32.SetConsoleCursorPosition(h, current_position)
        except Exception as e:
            return


if __name__ == '__main__':

    o = OptMatrix()
    o.listen()

