import cv2
import mediapipe as mp
import numpy as np
import sys

from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QMainWindow, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.addWidget(MainWindow())
# widget.setWindowIcon(logo_icon)
widget.setWindowTitle('SPARTAN')
# widget.show()
widget.showMaximized()

app.exec()