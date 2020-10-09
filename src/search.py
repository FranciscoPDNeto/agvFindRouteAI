#!/usr/bin/python3

import sys
import constant

class Output:
    def __init__(self, numSteps, numTimesPassedLocationPoint, coordsInitPoint):
        self.numSteps = numSteps
        self.numTimesPassedLocationPoint = numTimesPassedLocationPoint
        # Coordenadas representadas pela tupla (x,y)
        self.coordsInitPoint = coordsInitPoint
    
    def __str__(self):
        return "{} {} [{}, {}]".format(self.numSteps, self.numTimesPassedLocationPoint, \
            self.coordsInitPoint[0], self.coordsInitPoint[1])


algorithm = sys.argv[1]
entry = sys.argv[2]

fileEntry = open(entry, 'r')
x, y, w = [int(i) for i in next(fileEntry).split()]
map = [[i for i in line.rstrip('\n')] for line in fileEntry]

class State:
    def __init__(self, coord, cost):
        self.coord = coord
        self.cost = cost
    
    def __eq__(self, other):
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]

class Graph:
    def __init__(self, root, children):
        self.__init__(root, None, children)
    
    def __init__(self, root, parent):
        self.__init__(root, parent, None)
    
    def __init__(self, root, parent, children):
        self.root = root
        self.children = children
        self.parent = parent
        self.currentW = 0

    def addChild(self, move, cost, parent, explored):
        if (move[0] > 0 and move[0] < x and \
            move[1] > 0 and move[1 < y and \
            (move[0], move[1]) not in explored] and \
            (map[move[1]][move[0]] == constant.FREEPLACE and self.currentW < w or \
                map[move[1]][move[0]] == constant.LOCALIZATION_POINT)):

            self.children.append(State(move, cost))
            if (map[move[1]][move[0]] == constant.LOCALIZATION_POINT):
                self.currentW = 0

    def expandChildren(self, explored, goalPosition, heuristic = None):
        # Respectivamente CIMA, BAIXO, ESQUERDA, DIREITA.
        possibleMoves = [(self.root.coord[0], self.root.coord[1] - 1),\
            (self.root.coord[0], self.root.coord[1] + 1),\
            (self.root.coord[0] - 1, self.root.coord[1]),\
            (self.root.coord[0] + 1, self.root.coord[1])]
        
        if (not heuristic):
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1, self, explored)
        else:
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1 + heuristic(move, goalPosition), self, explored)


def bfsSearch():
    #TODO
    return "bfsSearch"

def dfsSearch():
    #TODO
    return "dfsSearch"

def idsSearch():
    #TODO
    return "idsSearch"

def aStarSearch():
    #TODO
    return "aStarSearch"

if (algorithm.lower() == "bfs"):
    bestRoute = bfsSearch()
elif (algorithm.lower() == "dfs"):
    bestRoute = dfsSearch()
elif (algorithm.lower() == "ids"):
    bestRoute = idsSearch()
elif (algorithm.lower() == "a*"):
    bestRoute = aStarSearch()
else:
    print("Wrong algorithm passed, please insert a valid one.")
    exit(1)

print(bestRoute)