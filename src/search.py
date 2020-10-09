#!/usr/bin/python3

import sys
import constant

class Output:
    def __init__(self, numSteps=0, numTimesPassedLocationPoint = 0, coordsInitPoint = (0,0)):
        self.numSteps = numSteps
        self.numTimesPassedLocationPoint = numTimesPassedLocationPoint
        # Coordenadas representadas pela tupla (linha,coluna)
        self.coordsInitPoint = coordsInitPoint
    
    def __str__(self):
        return "{} {} [{}, {}]".format(self.numSteps, self.numTimesPassedLocationPoint, \
            self.coordsInitPoint[0], self.coordsInitPoint[1])

def getPossibleStartCoords(width, height, map):
    possibleStartCoords = []
    for lineIdx, line in enumerate(map):
        for valueIdx, value in enumerate(line):
            if (lineIdx in [0, width - 1] or valueIdx in [0, height - 1]) and value != constant.OBSTACLE:
                possibleStartCoords.append(State((lineIdx, valueIdx), 0))
    
    return possibleStartCoords

                    

algorithm = sys.argv[1]
entry = sys.argv[2]

fileEntry = open(entry, 'r')
y, x, w = [int(i) for i in next(fileEntry).split()]
map = [[i for i in line.rstrip('\n')] for line in fileEntry]

class State:
    def __init__(self, coord : tuple, cost = 0):
        self.coord = coord
        self.cost = cost
        self.output = Output()
    
    def __eq__(self, other):
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]

class Graph:
    def __init__(self, root : State, parent = None, children : list = []):
        self.root = root
        self.children = children
        self.parent = parent
        self.currentW = 0

    def addChild(self, move : tuple, cost, parent, explored : list) -> None:
        if (move[0] > 0 and move[0] < y and \
            move[1] > 0 and move[1] < x and \
            (move[0], move[1]) not in explored and \
            map[move[0]][move[1]] != constant.OBSTACLE):

            if self.currentW == w and map[move[0]][move[1]] != constant.LOCALIZATION_POINT:
                return None

            self.children.append(Graph(State(move, cost), parent))
            if (map[move[1]][move[0]] == constant.LOCALIZATION_POINT):
                self.currentW = 0

    def expandChildren(self, explored : list, heuristic : bool = False) -> None:
        # Respectivamente BAIXO, CIMA, ESQUERDA, DIREITA.
        possibleMoves = [(self.root.coord[0], self.root.coord[1] + 1),\
            (self.root.coord[0], self.root.coord[1] - 1),\
            (self.root.coord[0] - 1, self.root.coord[1]),\
            (self.root.coord[0] + 1, self.root.coord[1])]
        
        if (not heuristic):
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1, self, explored)
        else:
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1 + heuristic(move), self, explored)

        self.currentW += 1


def bfsSearch():
    #TODO
    return "bfsSearch"

def dfsSearch(currentGraph : Graph, maxDepth : int, explored : list) -> Output:
    currentState = currentGraph.root
    if map[currentState.coord[0]][currentState.coord[1]] == constant.COLLECT_POINT:
        return currentState.output

    if maxDepth == 0:
        return None

    explored.append((currentState.coord[0], currentState.coord[1]))

    currentGraph.expandChildren(explored)
    for child in currentGraph.children:
        print("Child ({}, {}) cost {}".format(child.root.coord[0], child.root.coord[1], child.root.cost))
        possibleGoal = dfsSearch(child, maxDepth - 1, explored)
        print("Possible goal {}".format(possibleGoal))
        if possibleGoal != None:
            return possibleGoal

def idsSearch():
    #TODO
    return "idsSearch"

def aStarSearch():
    #TODO
    return "aStarSearch"

bestRoute = None
if (algorithm.lower() == "bfs"):
    bestRoute = bfsSearch()
elif (algorithm.lower() == "dfs"):
    for initialState in getPossibleStartCoords(y, x, map):
        bestRoute = dfsSearch(Graph(initialState), float("Inf"), [])
        if bestRoute != None:
            break
elif (algorithm.lower() == "ids"):
    bestRoute = idsSearch()
elif (algorithm.lower() == "a*"):
    bestRoute = aStarSearch()
else:
    print("Wrong algorithm passed, please insert a valid one.")
    exit(1)

print(bestRoute)