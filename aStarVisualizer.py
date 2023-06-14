from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout
from user import User

class BoardWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("A Star Algorithm Visualizer")
        self.setGeometry(100, 100, 400, 400)
        self.grid_size = 50
        self.button_size = 10

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        
        spacing = 3  # Adjust the spacing value as desired
        layout.setSpacing(spacing)
        
        # Calculate the margins to evenly distribute spacing
        total_spacing = (self.grid_size - 1) * spacing
        side_length = self.grid_size * self.button_size + total_spacing
        margin = total_spacing // (self.grid_size * 2)
        layout.setContentsMargins(margin, margin, margin, margin)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = QPushButton()
                button.setFixedSize(self.button_size, self.button_size)
                button.setStyleSheet("background-color: grey;")
                layout.addWidget(button, row, col)

                button.clicked.connect(lambda _, button=button: self.change_square_color(button, user))

        # Set the window size to be a square
        self.setFixedSize(side_length, side_length)

        central_widget.setStyleSheet("background-color: black;")
        
        self.setStartAndFinishNodes(user)

    def change_square_color(self, button, user):
        if not self.isStartOrFinishNode(button, user):
            button.setStyleSheet("background-color: white;")

    def isStartOrFinishNode(self, button, user):
        startX, startY, endX, endY = user.returnNodes()
        row, col = self.getButtonPosition(button)
        return (row == startX and col == startY) or (row == endX and col == endY)

    def getButtonPosition(self, button):
        layout = self.centralWidget().layout()
        for row in range(layout.rowCount()):
            for col in range(layout.columnCount()):
                if layout.itemAtPosition(row, col).widget() == button:
                    return row, col
        return None, None

    def setStartAndFinishNodes(self, user):
        startX, startY, endX, endY = user.returnNodes()

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                square_button = self.centralWidget().layout().itemAtPosition(row, col).widget()
                if row == startX and col == startY:
                    square_button.setStyleSheet("background-color: green;")
                elif row == endX and col == endY:
                    square_button.setStyleSheet("background-color: red;")
                else:
                    square_button.setStyleSheet("background-color: grey;")
