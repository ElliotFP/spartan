import cv2
import mediapipe as mp
import numpy as np
import sys
import json

from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QMainWindow, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal


class AlarmList(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarmList.ui', self)
        
        self.nextAlarmIndex = 0
        self.deleteIndex = None
        self.labelTimes = [self.labelTime0, self.labelTime1, self.labelTime2, self.labelTime3]
        self.labelExtremes = [self.labelExtreme0, self.labelExtreme1, self.labelExtreme2, self.labelExtreme3]
        self.labelLights = [self.labelLights0, self.labelLights1, self.labelLights2, self.labelLights3]
        self.labelVoices = [self.labelVoice0, self.labelVoice1, self.labelVoice2, self.labelVoice3]
        self.btnActives = [self.btnActive0, self.btnActive1, self.btnActive2, self.btnActive3]

        for i in range(4):
            self.btnActives[i].clicked.connect(lambda: self.setActive(self.btnActives[i]))
    
    def refresh(self):
        with open('alarms.json') as f:
            self.data = json.load(f)
        
        self.numOfAlarms = self.alarmList['numOfAlarms']
        
        for i in range(self.numOfAlarms):
            alarm = self.alarmList[str(i)]
            if alarm['active']:
                self.labelTimes[self.nextAlarmIndex].setText(f"Time: {alarm['time']}")
                self.labelExtremes[self.nextAlarmIndex].setText(alarm['extreme'])

                music = alarm['music']
                brightness = alarm['brightness']
                colors = alarm['colors']
                self.labelLights[self.nextAlarmIndex].setText(f"Music: {music}, Brightness: {brightness}, Colors: {colors}")
                self.labelVoices[self.nextAlarmIndex].setText(alarm['voice'])
                
                if alarm['active']:
                    self.btnActives[self.nextAlarmIndex].setText("Active")
            
    
    

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.addWidget(AlarmList())
# widget.setWindowIcon(logo_icon)
widget.setWindowTitle('SPARTAN')
widget.show()

app.exec()