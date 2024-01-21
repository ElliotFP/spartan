import sys
import asyncio
import concurrent.futures
import json
import os
import time
import pygame
from PushUpCounter import PushUpCounter
from lightControls import start_strobe, stop_strobe

pygame.mixer.init()

# Read JSON file for settings
with open("alarms.json") as json_file:
    data = json.load(json_file)

json_num = sys.argv[1]  # int for alarm number

extreme_mode = data[json_num]["extreme"]  # number of pushups or squats
lights_brightness = data[json_num]["brightness"]
lights_color = data[json_num]["colors"]
alarm_sound = data[json_num]["music"]
speech_text = data[json_num]["voice"]

colorDict = {
    "red": (255, 0, 0),
    "green": (0,128,0),
    "blue": (65,105,225),
    "yellow": (255, 255, 0),
    "orange": (255, 69, 0),
    "brown": (139,69,19)
}

async def alarm_sequence():
    if speech_text!=None:
        print("Playing speech")
        song = pygame.mixer.music.load(speech_text)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(100)
    # Play alarm sound
    if alarm_sound!=None:
        print("Playing alarm sound")
        song = pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play()
    
    # Start light strobe
    brightness = 200  # Example brightness
    frequency = 0.5   # Example frequency in seconds
    colors = []
    for color in lights_color:
        colors.append(colorDict[color])
        
    strobe_task, led = await start_strobe(brightness, frequency, colors)

    # Start pushup counter and wait for it to finish
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, lambda: PushUpCounter.start_pushup_counter(extreme_mode))
        print(result)

    # Stop light strobe after pushup counter finishes
    await stop_strobe(strobe_task, led)

    # Stop alarm sound
    if alarm_sound!=None and os.path.isfile(alarm_sound):
        song.stop()

if __name__ == '__main__':
    asyncio.run(alarm_sequence())
