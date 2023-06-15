import sys
from user import User
from aStarVisualizer import Visualizer

if __name__ == "__main__":
    user = User()
    user.startUp()

    grid = Visualizer(800, 800, 15, 2)
    grid.run(user)
