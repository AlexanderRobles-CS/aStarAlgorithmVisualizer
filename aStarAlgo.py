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

    def findSmallestFCost(self):
        smallestVal = self.OPEN[0][1]
        smallestIndex = 0

        for index, node in enumerate(self.OPEN):
            f_Cost = node[1]
            if f_Cost < smallestVal:
                smallestVal = f_Cost
                smallestIndex = index

        return self.OPEN[smallestIndex], smallestIndex
    
    def computeNeighbors(self, q):
        neighbors = []

        # left neighbor
        # upper neighbor
        # right neighbor
        # bottom neighbor

        return neighbors
    
    def generateSuccessors(self, q):
        successors = []                                # initialize successors

        neighbors = self.computeNeighbors(q)

    
    def runAlgo(self, grid):
        self.map = grid.grid                            # get grid 

        self.OPEN.append((grid.start, 0))               # put starting node in OPENLIST with f_score of 0

        self.q, popQIndex = self.findSmallestFCost()
        self.OPEN.pop(popQIndex)
        

        while len(self.OPEN) > 0:                                     # while OPEN list is not empty
            self.q, smallestIndex = self.findSmallestFCost()          # find the node with the smallest f_score in the open list

            self.OPEN.pop(smallestIndex)                              # pop q off the OPEN list
            self.generateSuccessors(self.q)                                 # generate q's 8 successors and set their parents to q






        



