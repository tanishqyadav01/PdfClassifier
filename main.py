import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QFont, QMovie
from PyQt5.QtCore import Qt
import subprocess
import keyboard

class GradientWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Coding Titans UI')
        self.setGeometry(100, 100, 500, 500)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        heading_label = QLabel('Pdf Classifier', self)
        description_label = QLabel('With a user-friendly interface, our bot allows users to easily customize and expand the predefined categories, <br> tailoring the classification process to specific organizational needs.', self)
        status_label = QLabel('Bot is Running...', self)
        team_label = QLabel('BY - Coding Titans', self)

        self.set_label_style(heading_label, 40, 'bold', 'white', 'Arial', Qt.AlignCenter)
        self.set_label_style(description_label, 16, 'normal', 'white', 'Verdana', Qt.AlignCenter)
        self.set_label_style(status_label, 20, 'normal', 'white', 'Arial', Qt.AlignCenter)
        self.set_label_style(team_label, 16, 'normal', 'white', 'Verdana', Qt.AlignCenter)

        layout.addWidget(heading_label)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(description_label)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(status_label)

        gif_label = QLabel(self)
        movie = QMovie("loading.gif")
        gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(gif_label, alignment=Qt.AlignCenter)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addWidget(team_label)

        self.set_gradient_background()

        keyboard.add_hotkey('ctrl+p', self.run_python_file)

    def set_label_style(self, label, font_size, font_weight, text_color, font_family, alignment):
        font = QFont(font_family)
        font.setPointSize(font_size)
        font.setBold(font_weight == 'bold')
        label.setFont(font)
        label.setStyleSheet(f'color: {text_color};')
        label.setAlignment(alignment)

    def set_gradient_background(self):
        palette = QPalette()
        gradient = QColor(224, 224, 224)  
        gradient.setNamedColor("#3498db")  
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def run_python_file(self):
        subprocess.run(['python', 'model.py'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GradientWindow()
    window.show()
    sys.exit(app.exec_())
