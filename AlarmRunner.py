import sys
import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import json
from PushUpCounter import PushUpCounter

pygame.init() # initialize pygame

# read json file for settings
with open("alarms.json") as json_file:
    data = json.load(json_file)

json_num = sys.argv[1] # int for alarm number


extreme_mode = data[json_num]["extreme"] # number of pushups
lights_brightness = data[json_num]["brightness"] # int for brightness
lights_color = data[json_num]["colors"] # string for color
alarm_sound = data[json_num]["music"] # string for alarm sound
speech_text = data[json_num]["voice"] # string for speech text

if (alarm_sound != ""):
    print("alarm sound is " + alarm_sound)

    if (speech_text != ""):
        print("speech text is " + speech_text)
    
    # play alarm sound
    if (os.path.isfile(alarm_sound)):
        song = pygame.mixer.Sound(alarm_sound)
        song.play()
    elif (os.path.isdir(alarm_sound)):
        print("alarm sound is a directory")
        # play all .mp3 files in directory

    if extreme_mode:
        print("extreme mode")
        PushUpCounter.start_pushup_counter(extreme_mode)
        
        # stop alarm sound
        song.stop()

# Lights Section

if (lights_brightness > 0):
    print("lights on")
    if lights_mode == 0:
        print("lights mode is solid")
        

else:
    print("no alarm sound")