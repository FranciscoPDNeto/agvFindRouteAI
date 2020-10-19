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
industryMap = [[i for i in line.rstrip('\n')] for line in fileEntry]

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
            industryMap[move[0]][move[1]] != constant.OBSTACLE):

            if self.root.currentW == w and industryMap[move[0]][move[1]] != constant.LOCALIZATION_POINT:
                return None

            numTimesPassedLocationPoint = self.root.output.numTimesPassedLocationPoint + \
                (1 if industryMap[move[0]][move[1]] == constant.LOCALIZATION_POINT else 0)
            currentW = self.root.currentW + \
                (1 if industryMap[move[0]][move[1]] != constant.LOCALIZATION_POINT else -1*self.root.currentW)

            output = Output(self.root.output.numSteps + 1, numTimesPassedLocationPoint, self.root.output.coordsInitPoint)
            child = Graph(State(move, cost, currentW, output), [], self)
            self.children.append(child)

    def __str__(self):
        return "State {} from parent {} from children {}".format(self.root.coord, self.parent, self.children)

    def expandChildren(self, explored : list, heuristic = None) -> None:
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
                self.addChild(move, self.root.cost + 1 + heuristic(move), explored)

def getGoalCoords(industryMap) -> tuple:
    for lineIdx, line in enumerate(industryMap):
        for valueIdx, value in enumerate(line):
            if value == constant.COLLECT_POINT:
                return (lineIdx, valueIdx)
    raise Exception("There's no collect point in the map.")

def getInitialGraph(width, height, industryMap) -> Graph:
    possibleStartGraphs = []
    for lineIdx, line in enumerate(industryMap):
        for valueIdx, value in enumerate(line):
            if (lineIdx in [0, width - 1] or valueIdx in [0, height - 1]) and value != constant.OBSTACLE:
                coord = (lineIdx, valueIdx)
                possibleStartGraphs.append(Graph(State(coord, 1, 0, \
                    Output(1, 1 if value == constant.LOCALIZATION_POINT else 0, coord)), []))

    return Graph(State((-2, -2)), possibleStartGraphs)


def bfsSearch(graph : Graph) -> Output:
    visitedNodesCoords = []
    nodesQueue = graph.children

    while nodesQueue:
        node = nodesQueue.pop(0)
        currentState = node.root
        if currentState.coord[0] >= 0 and industryMap[currentState.coord[0]][currentState.coord[1]] == constant.COLLECT_POINT:
            return currentState.output
        visitedNodesCoords.append(currentState.coord)
        node.expandChildren(visitedNodesCoords)
        nodesQueue = nodesQueue + node.children

def dlsSearch(currentGraph : Graph, maxDepth : int, explored : list) -> Output:
    currentState = currentGraph.root
    if currentState.coord[0] >= 0 and industryMap[currentState.coord[0]][currentState.coord[1]] == constant.COLLECT_POINT:
        return currentState.output

    if maxDepth == 0:
        return None

    explored.append(currentState.coord)

    currentGraph.expandChildren(explored)
    for child in currentGraph.children:
        possibleGoal = dlsSearch(child, maxDepth - 1, explored)
        if possibleGoal != None:
            return possibleGoal

def dfsSearch(currentGraph : Graph, explored : list) -> Output:
    return dlsSearch(currentGraph, float('Inf'), [])

def idsSearch(initialGraph : Graph, maxDepth : int) -> Output:

    for depth in range(int(maxDepth)):
        explored = []
        output = dlsSearch(initialGraph, depth, explored)
        if output:
            return output
        # Reinicializa o grafo inicial para os primeiros valores para a próxima
        # iteração.
        initialGraph = getInitialGraph(y, x, industryMap)

    return None

def aStarSearch(graph):
    goalCoords = getGoalCoords(industryMap)
    # Define a heurística do A*, que será a Distância de Manhattan.
    manhattanDistanceHeuristic = lambda move : abs(move[0] - goalCoords[0]) + abs(move[1] - goalCoords[1])

    visitedNodesCoords = []
    nodesList = graph.children

    while nodesList:
        # Busca e remove o nó expandido com o menor custo atualmente.
        node = min(nodesList, key=lambda node: node.root.cost)
        nodesList.remove(node)
        currentState = node.root
        if currentState.coord[0] >= 0 and industryMap[currentState.coord[0]][currentState.coord[1]] == constant.COLLECT_POINT:
            return currentState.output
        visitedNodesCoords.append(currentState.coord)
        node.expandChildren(visitedNodesCoords, manhattanDistanceHeuristic)
        nodesList = nodesList + node.children

bestRoute = None
initialGraph = getInitialGraph(y, x, industryMap)
if (algorithm.lower() == "bfs"):
    bestRoute = bfsSearch(initialGraph)
elif (algorithm.lower() == "dfs"):
    bestRoute = dfsSearch(initialGraph, [])
elif (algorithm.lower() == "ids"):
    bestRoute = idsSearch(initialGraph, y * x)
elif (algorithm.lower() == "a_star"):
    bestRoute = aStarSearch(initialGraph)
else:
    print("Wrong algorithm passed, please insert a valid one.")
    exit(1)

print(bestRoute)
