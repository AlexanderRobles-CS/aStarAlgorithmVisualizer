import sys
import re
from PyQt6 import QtWidgets

class User:
    def __init__(self):
        self.startX = 0
        self.startY = 0
        self.endX = 0
        self.endY = 0

    def extract_coordinates(self, point_string):
        pattern = r'\((-?\d+),(-?\d+)\)'
        match = re.search(pattern, point_string)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            return x, y
        else:
            return None

    def save_text(self, text_edit_1, text_edit_2):
        input_text_1 = text_edit_1.toPlainText().strip()
        self.startX, self.startY = self.extract_coordinates(input_text_1)

        if self.startX is None or self.startY is None:
            print("Invalid start node")
            return
        
        input_text_2 = text_edit_2.toPlainText().strip()
        self.endX, self.endY = self.extract_coordinates(input_text_2)

        if self.endX is None or self.endY is None:
            print("Invalid end node")
            return

        print(f"Start Node: ({self.startX}, {self.startY})")
        print(f"End Node: ({self.endX}, {self.endY})")

    def startUp(self):
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()
        window.setWindowTitle("Two Text Fields")
        window.setGeometry(100, 100, 400, 200)
        window.setFixedSize(400, 200)

        central_widget = QtWidgets.QWidget(window)
        window.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        text_edit_1 = QtWidgets.QTextEdit()
        text_edit_1.setFixedHeight(50)
        text_edit_1.setPlaceholderText("Start Node: (x,y)")
        layout.addWidget(text_edit_1)

        layout.addSpacing(10)

        text_edit_2 = QtWidgets.QTextEdit()
        text_edit_2.setFixedHeight(50)
        text_edit_2.setPlaceholderText("End Node: (x,y)")
        layout.addWidget(text_edit_2)

        button = QtWidgets.QPushButton("Save")
        button.clicked.connect(lambda _, t1=text_edit_1, t2=text_edit_2: self.save_text(t1, t2))
        layout.addWidget(button)

        window.show()

        sys.exit(app.exec())