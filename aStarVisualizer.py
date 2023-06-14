from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QGridLayout

class BoardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A Star Algorithm Visualizer")
        self.setGeometry(100, 100, 400, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        
        grid_size = 50
        button_size = 10
        
        spacing = 3  # Adjust the spacing value as desired
        layout.setSpacing(spacing)
        
        # Calculate the margins to evenly distribute spacing
        total_spacing = (grid_size - 1) * spacing
        side_length = grid_size * button_size + total_spacing
        margin = total_spacing // (grid_size * 2)
        layout.setContentsMargins(margin, margin, margin, margin)

        for row in range(grid_size):
            for col in range(grid_size):
                button = QPushButton()
                button.setFixedSize(button_size, button_size)
                button.setStyleSheet("background-color: grey;")
                layout.addWidget(button, row, col)

                button.clicked.connect(lambda _, button=button: self.change_square_color(button))

        # Set the window size to be a square
        self.setFixedSize(side_length, side_length)

    def change_square_color(self, button):
        button.setStyleSheet("background-color: white;")
