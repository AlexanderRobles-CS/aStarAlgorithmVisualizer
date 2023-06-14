import sys
from user import User
from aStarVisualizer import BoardWindow
from PyQt6.QtWidgets import QApplication


if __name__ == "__main__":

    user = User()
    user.startUp()
    
    app = QApplication(sys.argv)
    window = BoardWindow()
    window.show()
    
    sys.exit(app.exec())