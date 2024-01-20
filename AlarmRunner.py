import sys
import cv2
import mediapipe as mp
import numpy as np
import pygame   
import os
from PushUpCounter import PushUpCounter

pygame.init() # initialize pygame


extreme_mode = sys.argv[1] # 0 for normal, 1 for extreme
print("extreme_mode is" + extreme_mode)

lights_brightness = sys.argv[2] # int for brightness level
lights_color = sys.argv[3] # int for color
lights_mode = sys.argv[4] # int for mode
print("lights_brightness is " + lights_brightness + ", lights_color is " + lights_color + ", lights_mode is " + lights_mode)

alarm_sound = sys.argv[5] # string for .mp3 file
print("alarm_sound is " + alarm_sound)

speech_text = sys.argv[6] # string for text to speech
print("speech_text is " + speech_text)

if (alarm_sound != ""):
    print("alarm sound is " + alarm_sound)
    
    # play alarm sound
    if (os.path.isfile(alarm_sound)):
        song = pygame.mixer.Sound(alarm_sound)
        song.play()
    #elif (os.path.isdir(alarm_sound)):
    #    print("alarm sound is a directory")

        # play all .mp3 files in directory
        

    if extreme_mode:
        print("extreme mode")
        num_pushups = int(sys.argv[7]) # int for number of pushups
        PushUpCounter.start_pushup_counter(num_pushups)
        
        # stop alarm sound
        song.stop()

# Lights Section

if (lights_brightness > 0):
    print("lights on")
    if lights_mode == 0:
        print("lights mode is solid")
        

else:
    print("no alarm sound")