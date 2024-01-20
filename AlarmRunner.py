import sys
import cv2
import mediapipe as mp
import numpy as np
from PushUpCounter import PushUpCounter

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

if (extreme_mode): # code for running the PushupCounter.py script
    num_pushups = int(sys.argv[7]) # int for number of pushups
    print("extreme mode")

    PushUpCounter.start_pushup_counter(num_pushups)
else:
    print("normal mode")


