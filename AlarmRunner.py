import sys
import asyncio
import concurrent.futures
import json
import os
import pygame
from PushUpCounter import PushUpCounter
from lightControls import start_strobe, stop_strobe

pygame.init()

# Read JSON file for settings
with open("alarms.json") as json_file:
    data = json.load(json_file)

json_num = sys.argv[1]  # int for alarm number

extreme_mode = data[json_num]["extreme"]  # number of pushups or squats
lights_brightness = data[json_num]["brightness"]
lights_color = data[json_num]["colors"]
alarm_sound = data[json_num]["music"]
speech_text = data[json_num]["voice"]

async def alarm_sequence():
    # Play alarm sound
    if alarm_sound!=None:
        print("Playing alarm sound")
        song = pygame.mixer.Sound(alarm_sound)
        song.play()
    
    # Start light strobe
    brightness = 200  # Example brightness
    frequency = 0.5   # Example frequency in seconds
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Example colors
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
