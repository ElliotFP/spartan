from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

authenticator = IAMAuthenticator('fiTf2BjX2JMom2WqDSI8ATeUj9dPH0UIyKlUiEMnhFO1')
text_to_speech = TextToSpeechV1(authenticator=authenticator)

text_to_speech.set_service_url('https://api.us-east.text-to-speech.watson.cloud.ibm.com/instances/40fbddea-d2a5-4314-95c6-ca74b8267155')

# Convert a string
with open('good_morning.mp3', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            "Croatia is cringe",
            voice='en-GB_JamesV3Voice',
            accept='audio/mp3'
        ).get_result().content)

os.system("start good_morning.mp3")
