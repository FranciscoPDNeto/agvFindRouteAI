#!/usr/bin/python3

import sys

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

print(map)

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