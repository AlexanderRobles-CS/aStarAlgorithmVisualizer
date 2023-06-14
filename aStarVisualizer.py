from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt6.QtCore import Qt


class CustomButton(QPushButton):
    def __init__(self, board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.user = None

    def setUser(self, user):
        self.user = user

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_square_color()
            self.board.mouse_pressed = True

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.board.mouse_pressed:
            self.change_square_color()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.board.mouse_pressed = False

    def change_square_color(self):
        if not self.isStartOrFinishNode():
            self.setStyleSheet("background-color: white;")

    def isStartOrFinishNode(self):
        startX, startY, endX, endY = self.user.returnNodes()
        row, col = self.board.getButtonPosition(self)
        return (row == startX and col == startY) or (row == endX and col == endY)


class BoardWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("A Star Algorithm Visualizer")
        self.setGeometry(100, 100, 400, 400)
        self.grid_size = 50
        self.button_size = 10
        self.mouse_pressed = False

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
                button = CustomButton(self, self)
                button.setFixedSize(self.button_size, self.button_size)
                button.setStyleSheet("background-color: grey;")
                layout.addWidget(button, row, col)

                button.clicked.connect(button.change_square_color)
                button.setUser(user)
                button.installEventFilter(self)

        # Set the window size to be a square
        self.setFixedSize(side_length, side_length)

        central_widget.setStyleSheet("background-color: black;")

        self.setStartAndFinishNodes(user)

    def change_square_color(self, button):
        if not button.isStartOrFinishNode():
            button.setStyleSheet("background-color: white;")

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

    def eventFilter(self, obj, event):
        if event.type() == event.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            button = obj
            self.change_square_color(button)
        elif event.type() == event.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = False
        elif event.type() == event.Type.MouseMove and self.mouse_pressed:
            button = self.childAt(event.pos())
            if isinstance(button, CustomButton):
                self.change_square_color(button)
        return super().eventFilter(obj, event)
