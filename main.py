import cv2
import mediapipe as mp
import numpy as np
import sys

from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QMainWindow, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal


app = QApplication(sys.argv)
widget = QStackedWidget()
widget.addWidget(sterilizationWindow)
widget.setWindowIcon(logo_icon)
widget.setWindowTitle('Sterilization DB')