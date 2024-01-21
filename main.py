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
        
        self.data = None
        self.nextAlarmIndex = 0
        self.alarmIndexes = []
        self.cards = [self.card0, self.card1, self.card2, self.card3]
        self.labelTimes = [self.labelTime0, self.labelTime1, self.labelTime2, self.labelTime3]
        self.labelExtremes = [self.labelExtreme0, self.labelExtreme1, self.labelExtreme2, self.labelExtreme3]
        self.labelLights = [self.labelLights0, self.labelLights1, self.labelLights2, self.labelLights3]
        self.labelVoices = [self.labelVoice0, self.labelVoice1, self.labelVoice2, self.labelVoice3]
        self.btnActives = [self.btnActive0, self.btnActive1, self.btnActive2, self.btnActive3]
        self.btnDeletes = [self.btnDelete0, self.btnDelete1, self.btnDelete2, self.btnDelete3]
        self.btnNew.clicked.connect(self.newAlarm)

        for i in range(4):
            self.btnActives[i].clicked.connect(lambda _, i=i: self.setActive(i))
            self.btnDeletes[i].clicked.connect(lambda _, i=i: self.deleteAlarm(i))
        
        self.refresh()
    
    def newAlarm(self):

    
    def refresh(self):
        self.nextAlarmIndex = 0
        self.alarmIndexes = []
        with open('alarms.json') as f:
            self.alarmList = json.load(f)
        
        self.numberOfAlarms = self.alarmList['numberOfAlarms']
        
        for i in range(self.numberOfAlarms):
            self.alarmIndexes.append(i)
            self.cards[self.nextAlarmIndex].show()
            alarm = self.alarmList[str(i)]
            self.labelTimes[self.nextAlarmIndex].setText(f"Time: {alarm['time']}")
            self.labelExtremes[self.nextAlarmIndex].setText(str(alarm['extreme']))

            music = alarm['music']
            brightness = alarm['brightness']
            colors = ', '.join(alarm['colors'])
            self.labelLights[self.nextAlarmIndex].setText(f"Music: {music}\nBrightness: {brightness}\nColors: {colors}")
            self.labelVoices[self.nextAlarmIndex].setText(alarm['voice'])

            if alarm['active']:
                self.btnActives[self.nextAlarmIndex].setText('  Active')
                self.btnActives[self.nextAlarmIndex].setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(0, 234, 164);background-color: rgb(22, 39, 95);color: rgb(255, 255, 255);")
                self.btnActives[self.nextAlarmIndex].setIcon(QIcon('UI/active.png'))
            else:
                self.btnActives[self.nextAlarmIndex].setText('  Inactive')
                self.btnActives[self.nextAlarmIndex].setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(234, 0, 49);background-color: rgb(22, 39, 95);color: rgb(255, 255, 255);")
                self.btnActives[self.nextAlarmIndex].setIcon(QIcon('UI/inactive.png'))
            self.nextAlarmIndex += 1
        
        i = self.nextAlarmIndex
        while i < 4:
            self.cards[i].hide()
            i += 1
    

    def setActive(self, index):
        alarm = self.alarmList[str(index)]
        if alarm['active']:
            self.btnActives[index].setText('  Inactive')
            self.btnActives[index].setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(234, 0, 49);background-color: rgb(22, 39, 95);color: rgb(255, 255, 255);")
            self.btnActives[index].setIcon(QIcon('UI/inactive.png'))
            alarm['active'] = False
        else:
            self.btnActives[index].setText('  Active')
            self.btnActives[index].setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(0, 234, 164);background-color: rgb(22, 39, 95);color: rgb(255, 255, 255);")
            self.btnActives[index].setIcon(QIcon('UI/active.png'))
            alarm['active'] = True
        self.alarmList[str(index)] = alarm
        with open('alarms.json', 'w') as f:
            json.dump(self.alarmList, f, indent=4)


    def deleteAlarm(self, index):
        for i in range(index, self.numberOfAlarms-1):
            self.alarmList[str(i)] = self.alarmList[str(i + 1)]
        self.numberOfAlarms -= 1
        self.alarmList['numberOfAlarms'] = self.numberOfAlarms
        with open('alarms.json', 'w') as f:
            json.dump(self.alarmList, f, indent=4)
        
        self.refresh()

class NewAlarm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarm.ui', self)

    

app = QApplication(sys.argv)
widget = QStackedWidget()
widget.addWidget(AlarmList())
widget.addWidget(NewAlarm())
# widget.setWindowIcon(logo_icon)
widget.setWindowTitle('SPARTAN')
widget.show()

app.exec()