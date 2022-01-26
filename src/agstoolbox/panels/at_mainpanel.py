from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 172))
        self.setWindowTitle("Set Account")

        # Setup username field
        self.username_label = QLabel(self)
        self.username_label.setText('Username')
        self.username_field = QLineEdit(self)
        self.username_label.move(45, 20)
        self.username_field.move(115, 23)
        self.username_field.resize(150, 25)

        # Setup OK button
        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.buttonClicked)
        pybutton.resize(100, 32)
        pybutton.move(110, 128)

    def buttonClicked(self):
        print('Username: ' + self.username_field.text())
