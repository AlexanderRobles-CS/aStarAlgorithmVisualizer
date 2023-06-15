import re

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
        self.q = None

    def extract_coordinates(self, point_string):
        pattern = r'\((-?\d+), (-?\d+)\)'  # Pattern to match the coordinates inside parentheses

        match = re.search(pattern, point_string)
        if match:
            x = int(match.group(1))  # Extract the first captured group as an integer
            y = int(match.group(2))  # Extract the second captured group as an integer
            return x, y
        else:
            return None

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

        x, y = self.extract_coordinates(str(self.q[0]))

        neighbors.append((x - 1, y - 1))        # top left
        neighbors.append((x - 1, y))            # top
        neighbors.append((x - 1, y + 1))        # up right
        neighbors.append((x, y + 1))            # right
        neighbors.append((x + 1, y + 1))        # down right
        neighbors.append((x + 1, y))            # down
        neighbors.append((x + 1, y - 1))        # down left
        neighbors.append((x, y - 1))            # left

        print("NEIGHBORS: " + str(neighbors))

        return neighbors
    
    def returnValidNeighbors(self, neighbors):
        validNeighbors = []

        for neighbor in neighbors:
            x, y = neighbor

            if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]):
                validNeighbors.append(neighbor)

        return validNeighbors

    
    def generateSuccessors(self):
        successors = []                                # initialize successors
        neighbors = self.computeNeighbors()
        validNeighbors = self.returnValidNeighbors(neighbors)
        print("VALID NEIGHBORS" + str(validNeighbors))
    
    def runAlgo(self, grid):
        self.map = grid.grid                            # get grid 

        self.OPEN.append((grid.start, 0))               # put starting node in OPENLIST with f_score of 0

        self.q, popQIndex = self.findSmallestFCost()    # find the node with the smallest f_score

        self.generateSuccessors()       # filler

        self.OPEN.pop(popQIndex)
        

        # while len(self.OPEN) > 0:                                     # while OPEN list is not empty
        #     self.q, smallestIndex = self.findSmallestFCost()          # find the node with the smallest f_score in the open list

        #     self.OPEN.pop(smallestIndex)                              # pop q off the OPEN list
        #     # self.generateSuccessors(self.q)                                 # generate q's 8 successors and set their parents to q






        



