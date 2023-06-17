import re
import math

class Node:
    def __init__(self, position=None):
        self.position = position
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.parent = None

class neighbors:
    def __init__(self):
        self.north = None
        self.northEast = None
        self.East = None
        self.southEast = None
        self.south = None
        self.southWest = None
        self.west = None
        self.northWest = None

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
        # Check if the point_string is already in tuple format
        if isinstance(point_string, tuple):
            return str(point_string[0]), str(point_string[1])

        # Check if the point_string is in the format ((x, y), g)
        if point_string.startswith("((") and point_string.endswith(")"):
            coordinates = point_string[2:-1].split(",")
            position = coordinates[0].strip() + "," + coordinates[1].strip()
            x, y = self.extract_coordinates(position)
            return x, y

        # Extract the coordinates from the point_string
        coordinates = re.findall(r'\d+', point_string)
        return coordinates[0], coordinates[1]

    def findSmallestFCost(self):
        smallestIndex = 0
        smallestTuple = self.OPEN[0][0]
        smallestFCost = self.OPEN[0][1]

        for index, (node, f_Cost) in enumerate(self.OPEN):
            if f_Cost < smallestFCost:
                smallestFCost = f_Cost
                smallestTuple = node
                smallestIndex = index

        return smallestTuple, smallestIndex

    
    def computeNeighbors(self):
        neighbors_obj = neighbors()

        print("COMPUTE neighbors with q: " + str(self.q.position))
        x, y = self.extract_coordinates(str(self.q.position))
        print("x: " + str(x) + " y: " + str(y) + " inside computeNeighbors()")

        neighbors_obj.north = (int(x) - 1, int(y))
        neighbors_obj.northEast = (int(x) - 1, int(y) + 1)
        neighbors_obj.East = (int(x), int(y) + 1)
        neighbors_obj.southEast = (int(x) + 1, int(y) + 1)
        neighbors_obj.south = (int(x) + 1, int(y))
        neighbors_obj.southWest = (int(x) + 1, int(y) - 1)
        neighbors_obj.west = (int(x), int(y) - 1)
        neighbors_obj.northWest = (int(x) - 1, int(y) - 1)

        return neighbors_obj

    def addSuccessor(self, successor, grid):
        x, y = self.extract_coordinates(successor.position)
        print("x: " + str(x) + " y: " + str(y) + " inside addSuccessor()")

        if self.isValidPosition(x, y) and not self.isNodeInClosedList(x, y, grid):
            successor.gCost = self.q.gCost + self.distance(successor.position)
            successor.hCost = self.heuristicSuccessor(successor.position, grid)
            successor.fCost = successor.gCost + successor.hCost
            successor.parent = self.q.position
            self.OPEN.append((successor, successor.fCost))

    def isValidPosition(self, x, y):
        if 0 <= int(x) < 50 and 0 <= int(y) < 50 and self.map[int(x)][int(y)] != 3:
            return True
        return False

    def isNodeInClosedList(self, x, y, grid):
        for node in self.CLOSED:
            if node.position == (int(x), int(y)):
                return True
        return False

    def heuristicSuccessor(self, position, grid):
        nodeX, nodeY = self.extract_coordinates(str(self.current.position))
        nodeX = int(nodeX)  # Convert the string to int
        nodeY = int(nodeY)  # Convert the string to int

        goalX, goalY = self.extract_coordinates(str(grid))
        goalX = int(goalX)
        goalY = int(goalY)

        distance = abs(nodeX - goalX) + abs(nodeY - goalY)
        return distance


    def distance(self, position):
        x, y = self.extract_coordinates(str(position))
        return math.sqrt(int(x)**2 + int(y)**2)

    def runAlgo(self, grid, start, end):

        self.map = grid.grid
        self.current = Node(start)
        self.current.position = start
        print("self.current position: " + str(self.current.position))
        self.current.hCost = self.heuristicSuccessor(self.current.position, grid.end)
        self.OPEN.append((self.current, self.current.hCost))
        self.pathFound = False

        while not self.pathFound and len(self.OPEN) > 0:
            print("self.current position: " + str(self.q.position))
            self.q, qIndex = self.findSmallestFCost()
            self.OPEN.pop(qIndex)
            self.CLOSED.append(self.q)

            if self.q.position == end:
                self.pathFound = True
                print("Path found")
                return

            successorNodes = self.computeNeighbors()

            # North
            successor = Node(successorNodes.north)
            self.addSuccessor(successor, self.map)

            # North-East
            successor = Node(successorNodes.northEast)
            self.addSuccessor(successor, self.map)

            # East
            successor = Node(successorNodes.East)
            self.addSuccessor(successor, self.map)

            # South-East
            successor = Node(successorNodes.southEast)
            self.addSuccessor(successor, self.map)

            # South
            successor = Node(successorNodes.south)
            self.addSuccessor(successor, self.map)

            # South-West
            successor = Node(successorNodes.southWest)
            self.addSuccessor(successor, self.map)

            # West
            successor = Node(successorNodes.west)
            self.addSuccessor(successor, self.map)

            # North-West
            successor = Node(successorNodes.northWest)
            self.addSuccessor(successor, self.map)
