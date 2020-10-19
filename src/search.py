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


algorithm = sys.argv[1]
entry = sys.argv[2]

fileEntry = open(entry, 'r')
y, x, w = [int(i) for i in next(fileEntry).split()]
map = [[i for i in line.rstrip('\n')] for line in fileEntry]

class State:
    def __init__(self, coord : tuple, cost = 0, currentW = 0, output : Output = Output()):
        self.coord = coord
        self.cost = cost
        self.currentW = currentW
        self.output = output

    def __eq__(self, other):
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]

class Graph:
    def __init__(self, root : State, children : list, parent = None):
        self.root = root
        self.parent = parent
        self.children = children

    def addChild(self, move : tuple, cost : float, explored : list) -> None:
        if (move[0] > 0 and move[0] < y and \
            move[1] > 0 and move[1] < x and \
            (move not in explored) and \
            map[move[0]][move[1]] != constant.OBSTACLE):

            if self.root.currentW == w and map[move[0]][move[1]] != constant.LOCALIZATION_POINT:
                return None

            numTimesPassedLocationPoint = self.root.output.numTimesPassedLocationPoint + \
                (1 if map[move[0]][move[1]] == constant.LOCALIZATION_POINT else 0)
            currentW = self.root.currentW + \
                (1 if map[move[0]][move[1]] != constant.LOCALIZATION_POINT else -1*self.root.currentW)

            output = Output(self.root.output.numSteps + 1, numTimesPassedLocationPoint, self.root.output.coordsInitPoint)
            child = Graph(State(move, cost, currentW, output), [], self)
            self.children.append(child)

    def __str__(self):
        return "State {} from parent {} from children {}".format(self.root.coord, self.parent, self.children)

    def expandChildren(self, explored : list, heuristic : bool = False) -> None:
        # Respectivamente BAIXO, CIMA, ESQUERDA, DIREITA.
        possibleMoves = [(self.root.coord[0] + 1, self.root.coord[1]),\
            (self.root.coord[0] - 1, self.root.coord[1]),\
            (self.root.coord[0], self.root.coord[1] - 1),\
            (self.root.coord[0], self.root.coord[1] + 1)]

        if (not heuristic):
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1, explored)
        else:
            for move in possibleMoves:
                self.addChild(move, self.root.cost + 1 + heuristic(move), self, explored)


def getInitialGraph(width, height, map) -> Graph:
    possibleStartGraphs = []
    for lineIdx, line in enumerate(map):
        for valueIdx, value in enumerate(line):
            if (lineIdx in [0, width - 1] or valueIdx in [0, height - 1]) and value != constant.OBSTACLE:
                coord = (lineIdx, valueIdx)
                possibleStartGraphs.append(Graph(State(coord, 1, 0, \
                    Output(1, 1 if value == constant.LOCALIZATION_POINT else 0, coord)), []))

    return Graph(State((-2, -2)), possibleStartGraphs)


def bfsSearch():
    #TODO
    return "bfsSearch"

def dfsSearch(currentGraph : Graph, maxDepth : int, explored : list) -> Output:
    currentState = currentGraph.root
    if currentState.coord[0] >= 0 and map[currentState.coord[0]][currentState.coord[1]] == constant.COLLECT_POINT:
        return currentState.output

    if maxDepth == 0:
        return None

    explored.append(currentState.coord)

    currentGraph.expandChildren(explored)
    for child in currentGraph.children:
        possibleGoal = dfsSearch(child, maxDepth - 1, explored)
        if possibleGoal != None:
            return possibleGoal

def idsSearch(initialGraph : Graph, maxDepth : int) -> Output:

    for depth in range(int(maxDepth)):
        explored = []
        output = dfsSearch(initialGraph, depth, explored)
        if output:
            return output

    return None

def aStarSearch():
    #TODO
    return "aStarSearch"

bestRoute = None
if (algorithm.lower() == "bfs"):
    bestRoute = bfsSearch()
elif (algorithm.lower() == "dfs"):
    initialGraph = getInitialGraph(y, x, map)
    bestRoute = dfsSearch(initialGraph, float("Inf"), [])
elif (algorithm.lower() == "ids"):
    initialGraph = getInitialGraph(y, x, map)
    bestRoute = idsSearch(initialGraph, y * x)
elif (algorithm.lower() == "a_star"):
    bestRoute = aStarSearch()
else:
    print("Wrong algorithm passed, please insert a valid one.")
    exit(1)

print(bestRoute)
