# spartan

### Product Statement

Spartan is a platform for customizing your wake up experience with various different features.


## Functionality

-> Bluetooth connected LED controls for brightness, colour, mode (ex. music).

-> AI powered text-to-speech for reading motivational speeches or (not implemented yet) your notifications / the news.

-> Upload your own .mp3 file or files to play as the alarm.

-> List of your own alarm templates to choose from.

-> **(HARDCORE MODE)** Push-Up counter prevents the alarm from stopping until you do a set amount of push-ups.


## Implementation 

We are running our code on an orange pi, with an OV13850 camera, a 512 SSD and a wifi chip, running ubuntu 22.04. 


-> The bluetooth LEDs are from Govee, which has an easy-to-use python api to control them. 

-> The tts is implemented through *** .

-> We connected aux speakers and used the drivers provided by the orange pi's ubuntu image to output music to them.

-> The front-end UI is implemented through PyQT. 

-> We used a repo <a>https://github.com/aryanvij02/PushUpCounter</a> for the computer vision push up counter.


## Installation
Pip libraries:
- PyQt6
- bleak
- mediapipe
- govee-H613-BTcontroller
- opencv-python
- pygame
- ibm-watson
- ibm-cloud-sdk-core
- python-crontab
- paramiko
- scp