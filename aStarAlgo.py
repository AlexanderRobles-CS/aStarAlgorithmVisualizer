import re
import math
from node import Node

class AStar:
    """
    gCost = distance from starting node
    hCost = distance from ending node
    fCost = gCost + hCost
    """

    def __init__(self):
        self.OPEN = []                               # initialize OPEN list
        self.CLOSED = []                             # initialize CLOSED list
        self.map = None
        self.current = None
        self.pathFound = False
        self.q = Node()

    def extract_coordinates(self, point_string):
        pattern = r'\((-?\d+), (-?\d+)\)'  # Pattern to match the coordinates inside parentheses

        match = re.search(pattern, point_string)
        if match:
            x = int(match.group(1))  # Extract the first captured group as an integer
            y = int(match.group(2))  # Extract the second captured group as an integer
            return x, y
        else:
            return 0, 0  # Return default coordinates if no match is found
        
    def findSmallestFCost(self):
        smallestVal = self.OPEN[0][1]
        smallestIndex = 0

        for index, node in enumerate(self.OPEN):
            f_Cost = node[1]
            if f_Cost < smallestVal:
                smallestVal = f_Cost
                smallestIndex = index

        return self.OPEN[smallestIndex], smallestIndex
    
    def computeNeighbors(self):
        neighbors = []

        x, y = self.extract_coordinates(str(self.q.position[0]))

        neighbors.append((x - 1, y - 1))        # top left
        neighbors.append((x - 1, y))            # top
        neighbors.append((x - 1, y + 1))        # up right
        neighbors.append((x, y + 1))            # right
        neighbors.append((x + 1, y + 1))        # down right
        neighbors.append((x + 1, y))            # down
        neighbors.append((x + 1, y - 1))        # down left
        neighbors.append((x, y - 1))            # left

        return neighbors
    
    def returnValidNeighbor(self, neighbor):

        x, y = self.extract_coordinates(str(neighbor))

        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]) and self.map[x][y] != 3:        # check for boundaries and if it is a wall
            return True
        
        else:
            return False
        
    def checkClosedList(self, neighbor):
        x, y = self.extract_coordinates(str(neighbor))

        for pair in self.CLOSED:
            if pair[0] == x and pair[1] == y:
                return True
        else:
            return False
        
    def distance(self, neighbor):
        neighborX, neighborY = self.extract_coordinates(str(neighbor))
        nodeX, nodeY = self.extract_coordinates(str(self.q.position[0]))

        dx = abs(nodeX - neighborX)
        dy = abs(nodeY - neighborY)

        # return dx + dy                                                   # Manhattan distance (taxicab geometry)
    
        #  return max(dx, dy)                                              #  Chebyshev distance (maximum of horizontal and vertical differences)

        return math.sqrt(dx**2 + dy**2)                                    #  Euclidean distance
    

    def heuristic(self, grid):
        goalX, goalY = self.extract_coordinates(str(grid.end))
        nodeX, nodeY = self.extract_coordinates(str(self.q.position[0]))

        dx = abs(nodeX - goalX)                                          # Calculate the Euclidean distance between the node and the goal node
        dy = abs(nodeY - goalY)

        hCost = math.sqrt(dx**2 + dy**2)
    
        return hCost


    def generateSuccessors(self, grid):
        successors = []                                                    # initialize successors

        neighbors = self.computeNeighbors()                                # compute q's neighbors

        for neighbor in neighbors:
            isValidNeighbor = self.returnValidNeighbor(neighbor)           # return if it is a valid neighbor of q
            inClosedList = self.checkClosedList(neighbor)                  # return if neighbor is already in closed list

            if isValidNeighbor and not inClosedList:
                gCost = self.q.gCost + self.distance(neighbor)
                hCost = self.heuristic(grid)
                fCost = gCost + hCost
                successors.append((neighbor, fCost))
                self.q.parent = self.q.position                            # possible to change this later

        return successors

    
    def setPosition(self):
        self.q.position = self.q.position = self.q.position[0]
    
    def runAlgo(self, grid):
        self.map = grid.grid                            # get grid 

        self.OPEN.append((grid.start, 0))               # put starting node in OPENLIST with f_score of 0
        self.q.gCost = 0                                # set the starting node g cost to 0

        self.q.position, popQIndex = self.findSmallestFCost()    # find the node with the smallest f_score
        self.setPosition()

        successors = self.generateSuccessors(grid)       # filler

        print(successors)
        
        self.OPEN.pop(popQIndex)
        

        # while len(self.OPEN) > 0:                                     # while OPEN list is not empty
        #     self.q.position, smallestIndex = self.findSmallestFCost()          # find the node with the smallest f_score in the open list

        #     self.OPEN.pop(smallestIndex)                              # pop q off the OPEN list
        #     successors = self.generateSuccessors()                    # generate q's 8 successors and set their parents to q






        



