import mediapipe as mp
import numpy as np
import sys
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from PyQt6.QtWidgets import QApplication, QDialog, QStackedWidget, QMainWindow, QLabel, QTableWidgetItem, QAbstractItemView, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6 import uic

import paramiko
from scp import SCPClient


authenticator = IAMAuthenticator('fiTf2BjX2JMom2WqDSI8ATeUj9dPH0UIyKlUiEMnhFO1')
text_to_speech = TextToSpeechV1(authenticator=authenticator)

text_to_speech.set_service_url('https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/40fbddea-d2a5-4314-95c6-ca74b8267155')

def create_ssh_client(server, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def scp_transfer_file(ssh_client, local_path, remote_path):
    with SCPClient(ssh_client.get_transport()) as scp:
        scp.put(local_path, remote_path)

# Replace these with your Raspberry Pi details
server = '10.42.0.97'
port = 22  # default SSH port
username = 'root'  # default Raspberry Pi username
password = 'orangepi'  # password for SSH login

local_file = None  # File on your Ubuntu machine
remote_file = None # Destination on Raspberry Pi

# Create SSH client
ssh = create_ssh_client(server, port, username, password)


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
        self.btnAddAlarm.clicked.connect(self.addAlarm)

        for i in range(4):
            self.btnActives[i].clicked.connect(lambda _, i=i: self.setActive(i))
            self.btnDeletes[i].clicked.connect(lambda _, i=i: self.deleteAlarm(i))
        
        self.refresh()
    
    def addAlarm(self):
        widget.setCurrentIndex(1)

    
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
            self.labelExtremes[self.nextAlarmIndex].setText(f"Extreme: {str(alarm['extreme'])}")

            music = alarm['music'].split('/')[-1]
            brightness = alarm['brightness']
            colors = ', '.join(alarm['colors'])
            self.labelLights[self.nextAlarmIndex].setText(f"Music: {music}\nBrightness: {brightness}\nColors: {colors}")
            self.labelVoices[self.nextAlarmIndex].setText(alarm['voiceContent'])

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
        scp_transfer_file(ssh, '/home/roko/spartan/alarms.json', "/root/Desktop/spartan/alarms.json")


    def deleteAlarm(self, index):
        for i in range(index, self.numberOfAlarms-1):
            self.alarmList[str(i)] = self.alarmList[str(i + 1)]
        self.numberOfAlarms -= 1
        self.alarmList['numberOfAlarms'] = self.numberOfAlarms
        with open('alarms.json', 'w') as f:
            json.dump(self.alarmList, f, indent=4)
        
        scp_transfer_file(ssh, '/home/roko/spartan/alarms.json', "/root/Desktop/spartan/alarms.json")

        self.refresh()

class NewAlarm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('alarm.ui', self)
        self.isOrange = False
        self.isGreen = False
        self.isBlue = False
        self.isRed = False
        self.isYellow = False
        self.isBrown = False
        self.btnAlarms.clicked.connect(self.backToAlarms)
        self.btnSubmit.clicked.connect(self.submit)
        self.btnMusic.clicked.connect(self.selectMusic)
        self.btnOrange.clicked.connect(self.orange)
        self.btnGreen.clicked.connect(self.green)
        self.btnBlue.clicked.connect(self.blue)
        self.btnRed.clicked.connect(self.red)
        self.btnYellow.clicked.connect(self.yellow)
        self.btnBrown.clicked.connect(self.brown)
        self.fileDir = None
    
    def backToAlarms(self):
        alarmListWidget.refresh()
        widget.setCurrentIndex(0)
    
    def getColors(self):
        colors = []
        if self.isOrange:
            colors.append('orange')
        if self.isGreen:
            colors.append('green')
        if self.isBlue:
            colors.append('blue')
        if self.isRed:
            colors.append('red')
        if self.isYellow:
            colors.append('yellow')
        if self.isBrown:
            colors.append('brown')
        return colors
    

    def submit(self):
        if alarmListWidget.numberOfAlarms == 4:
            return
        with open('alarms.json') as f:
            self.alarmList = json.load(f)
        self.numberOfAlarms = self.alarmList['numberOfAlarms']
        highestVoice = 0
        for i in range(self.numberOfAlarms):
            if self.alarmList[str(i)]['voice'].split('.mp3')[0] == highestVoice:
                highestVoice += 1
        # Convert a string
        with open(f'voice/{highestVoice}.mp3', 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    self.voiceTxt.toPlainText(),
                    voice='en-GB_JamesV3Voice',
                    accept='audio/mp3'
                ).get_result().content)

        self.alarmList[str(self.numberOfAlarms)] = {
            'time': self.time.time().toString('hh:mm'),
            'extreme': self.extremeBox.value(),
            'colors': self.getColors(),
            'brightness': self.brightnessSlider.value(),
            'music': f"/root/Desktop/spartan/music/{self.fileDir[0].split('/')[-1]}",
            'voice': f"/root/Desktop/spartan/voice/{highestVoice}.mp3",
            'voiceContent': self.voiceTxt.toPlainText(),
            'active': True
        }
        self.numberOfAlarms += 1
        self.alarmList['numberOfAlarms'] = self.numberOfAlarms
        with open('alarms.json', 'w') as f:
            json.dump(self.alarmList, f, indent=4)
        
        scp_transfer_file(ssh, self.fileDir[0], f"/root/Desktop/spartan/music/{self.fileDir[0].split('/')[-1]}")
        scp_transfer_file(ssh, f'/home/roko/spartan/voice/{highestVoice}.mp3', f"/root/Desktop/spartan/voice/{highestVoice}.mp3")
        scp_transfer_file(ssh, '/home/roko/spartan/alarms.json', "/root/Desktop/spartan/alarms.json")
        self.backToAlarms()
    
    def selectMusic(self):
        self.fileDir = QFileDialog.getOpenFileName()
        self.musicTxt.setText(self.fileDir[0])
    
    def orange(self):
        if self.isOrange:
            self.btnOrange.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isOrange = False
        else:
            self.btnOrange.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(255, 85, 0);")
            self.isOrange = True

    def green(self):
        if self.isGreen:
            self.btnGreen.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isGreen = False
        else:
            self.btnGreen.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(0, 234, 164);")
            self.isGreen = True
    
    def blue(self):
        if self.isBlue:
            self.btnBlue.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isBlue = False
        else:
            self.btnBlue.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(0, 0, 255);")
            self.isBlue = True
    
    def red(self):
        if self.isRed:
            self.btnRed.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isRed = False
        else:
            self.btnRed.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(234, 0, 49);")
            self.isRed = True
    
    def yellow(self):
        if self.isYellow:
            self.btnYellow.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isYellow = False
        else:
            self.btnYellow.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(255, 255, 0);")
            self.isYellow = True
    
    def brown(self):
        if self.isBrown:
            self.btnBrown.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(36, 31, 49);background-color: rgb(245, 247, 248);")
            self.isBrown = False
        else:
            self.btnBrown.setStyleSheet("border-radius:6px;border-style: inset;border-width: 1.5px;border-color: rgb(22, 39, 95);color: rgb(255, 255, 255);background-color: rgb(128, 64, 0);")
            self.isBrown = True


app = QApplication(sys.argv)
widget = QStackedWidget()
alarmListWidget = AlarmList()
newAlarmWidget = NewAlarm()
widget.addWidget(alarmListWidget)
widget.addWidget(newAlarmWidget)
# widget.setWindowIcon(logo_icon)
widget.setWindowTitle('SPARTAN')
widget.show()

app.exec()