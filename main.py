import cv2
import mediapipe as mp
import numpy as np
import sys

from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QMainWindow, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal


class AlarmList(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarmList.ui', self)
    
    

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.addWidget(AlarmList())
# widget.setWindowIcon(logo_icon)
widget.setWindowTitle('SPARTAN')
widget.show()

app.exec()