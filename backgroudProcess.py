import json
import time
import os

playing = False

while True:
    with open('alarms.json') as json_file:
        data = json.load(json_file)
    
    numAlarms = data["numberOfAlarms"]
    for i in range(numAlarms):
        if data[str(i)]["active"]:
            if data[str(i)]["time"] == time.strftime("%H:%M"):
                print("Alarm!")
                if not playing:
                    playing = True
                    os.system("python3 AlarmRunner.py " + str(i))
            
            else:
                playing = False

    time.sleep(1)
