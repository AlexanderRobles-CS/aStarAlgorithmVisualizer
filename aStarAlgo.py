import re
import math

class Node:
    def __init__(self):
        self.position = None
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.parent = None

class Neighbor:
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
        print("point_string: " + str(point_string) + " inside extract_coordinates()")
        # Check if the point_string is in the format (x, y)
        if point_string.startswith("(") and point_string.endswith(")"):
            coordinates = point_string[1:-1].split(",")  # Remove parentheses and split coordinates
            x = str(coordinates[0]).replace("(", "")
            y = str(coordinates[1]).replace(")", "")
            return x, y

        # Check if the point_string is in the format ((x, y), g)
        elif point_string.startswith("((") and point_string.endswith(")"):
            coordinates = point_string[2:-1].split(",")  # Remove double parentheses and split coordinates
            position = coordinates[0] + "," + coordinates[1]  # Concatenate coordinates
            print("position: " + str(position) + " inside extract_coordinates()")
            x, y = self.extract_coordinates(position)  # Recursively extract coordinates
            return x, y

        # Raise an error if the point_string format is invalid
        raise ValueError("Invalid point string format")

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
        neighbor = Neighbor()

        print("COM{PUTE NEIGHBORS} with q: " + str(self.q.position))
        x, y = self.extract_coordinates(str(self.q.position))
        print("x: " + str(x) + " y: " + str(y) + " inside computeNeighbors()")

        neighbor.north = (x - 1, y)
        neighbor.northEast = (x - 1, y + 1)
        neighbor.East = (x, y + 1)
        neighbor.southEast = (x + 1, y + 1)
        neighbor.south = (x + 1, y)
        neighbor.southWest = (x + 1, y - 1)
        neighbor.west = (x, y - 1)
        neighbor.northWest = (x - 1, y - 1)

        return neighbor

    def returnValidNeighbor(self, position):
        print("position: " + str(position) + "inside returnValidNeighbor()")
        x, y = self.extract_coordinates(str(position))

        print("x: " + str(x) + " y: " + str(y) + " inside returnValidNeighbor()")

        if 0 <= x < len(self.map) and 0 <= y < len(self.map[0]) and self.map[x][y] != 3:
            return True
        else:
            return False

    def checkClosedList(self, neighbor):
        print("neighbor: " + str(neighbor) + "inside checkClosedList()")
        x, y = self.extract_coordinates(str(neighbor))

        print("x: " + str(x) + " y: " + str(y) + " inside checkClosedList()")

        for node in self.CLOSED:
            node_x, node_y = self.extract_coordinates(str(node))
            if node_x == x and node_y == y:
                return True
        return False

    def distance(self, neighbor):
        neighborX, neighborY = self.extract_coordinates(str(neighbor))
        nodeX, nodeY = self.extract_coordinates(str(self.q.position))

        dx = abs(nodeX - neighborX)
        dy = abs(nodeY - neighborY)

        return math.sqrt(dx**2 + dy**2)  # Euclidean distance

    def heuristic(self, grid):
        goalX, goalY = self.extract_coordinates(str(grid.end))
        nodeX, nodeY = self.extract_coordinates(str(self.q.position))

        dx = abs(nodeX - goalX)
        dy = abs(nodeY - goalY)

        hCost = math.sqrt(dx**2 + dy**2)

        return hCost

    def heuristicSuccessor(self, successor, grid):
        goalX, goalY = self.extract_coordinates(str(grid.end))
        nodeX, nodeY = self.extract_coordinates(str(successor))

        dx = abs(nodeX - goalX)
        dy = abs(nodeY - goalY)

        hCost = math.sqrt(dx**2 + dy**2)

        return hCost

    def generateSuccessors(self, grid):
        successors = []  # initialize successors

        neighbors = self.computeNeighbors()  # compute q's neighbors

        directions = ['north', 'northEast', 'East', 'southEast', 'south', 'southWest', 'west', 'northWest']
        for direction in directions:
                # Correct way to access neighbors
            if direction == 'north':
                position = neighbors.north
            elif direction == 'northEast':
                position = neighbors.northEast
            elif direction == 'East':
                position = neighbors.East
            elif direction == 'southEast':
                position = neighbors.southEast
            elif direction == 'south':
                position = neighbors.south
            elif direction == 'southWest':
                position = neighbors.southWest
            elif direction == 'west':
                position = neighbors.west
            elif direction == 'northWest':
                position = neighbors.northWest

            isValidNeighbor = self.returnValidNeighbor(position)
            inClosedList = self.checkClosedList(position)

            if isValidNeighbor and not inClosedList:
                successors.append(position)

        return successors

    def runAlgo(self, grid):
        self.q = Node()  # Initialize self.q as a Node object
        self.q.position = grid.start
        self.q.gCost = 0
        self.map = grid.grid
        self.OPEN.append((grid.start, 0))

        while len(self.OPEN) > 0:
            self.q.position, smallestIndex = self.findSmallestFCost()

            if self.q.position == grid.end:
                print("STOP SEARCH!")
                break

            self.OPEN.pop(smallestIndex)
            self.CLOSED.append(self.q.position)

            successors = self.generateSuccessors(grid)

            for successor in successors:
                print("successor: " + str(successor))
                fCost = self.q.gCost + self.distance(successor) + self.heuristicSuccessor(successor, grid)

                in_open = any(node.position == successor for node, _ in self.OPEN)
                in_closed = successor in self.CLOSED

                if in_open and in_closed:
                    continue

                if in_open:
                    open_node = next(node for node, _ in self.OPEN if node.position == successor)
                    if fCost < open_node.fCost:
                        open_node.gCost = self.q.gCost + self.distance(successor)
                        open_node.fCost = fCost
                        open_node.parent = self.q
                else:
                    successor_node = Node()
                    successor_node.position = successor
                    successor_node.gCost = self.q.gCost + self.distance(successor)
                    successor_node.fCost = fCost
                    successor_node.parent = self.q
                    self.OPEN.append((successor_node, fCost))

        print("FINAL NODE:", self.q)
        return self.q