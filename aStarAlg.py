import sys
from PyQt6.QtWidgets import QApplication
from user import User
from aStarVisualizer import BoardWindow

if __name__ == "__main__":
    user = User()
    user.startUp()

    app = QApplication(sys.argv)
    window = BoardWindow(user)
    window.show()

    sys.exit(app.exec())
