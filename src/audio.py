# Developed by Nalin Ahuja, nalinahuja

import sys

import pyaudio as pa
import audioop as ap

from time import time
from gpiozero import RGBLED
from colorzero import Color

# End Imports------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Audio Constants
SAMPLE_RATE = 44100
CHUNK_SIZE = 2048
MAX_VALUE = 1000

# Time Constants
BUFFER_TIME = 5.00
TIME_CONV = 16.67

# Process Lock File
LOCK_FILE = "./.lock"

# End Embedded Constants-------------------------------------------------------------------------------------------------------------------------------------------------------------

def normalize(value, min, max):
    # Normalize Input Value To Range [0, 1]
    return ((value - min) / (max - min + 1))

# End Helper Functions---------------------------------------------------------------------------------------------------------------------------------------------------------------

def init_leds():
    # Initialize GPIO Pins
    # leds = RGBLED(17, 22, 27)

    # Initialize Audio Interface
    source = pa.PyAudio()

    # Create Audio Stream
    stream = source.open(format = pa.paInt16, input = True, channels = 2, rate = SAMPLE_RATE, frames_per_buffer = CHUNK_SIZE)

    # Return Packed Data
    return (stream, None)

def animate_leds(stream, leds = None):
    # Create Process Lock File
    open(LOCK_FILE, "w")

    # Initialize Audio Score Metric
    audio_score = 0

    # Initialize Audio Frame Buffer
    frame_buffer, frame_buffer_size = [0], int(TIME_CONV * BUFFER_TIME)

    # Process Audio Stream
    while (True):
        # # Set LED Color By Audio Score
        # if (audio_score < 150):
        #     leds.color = Color("red")
        # elif (audio_score >= 150 and audio_score < 350):
        #     leds.color = Color("green")
        # elif (audio_score >= 350 and audio_score < 650):
        #     leds.color = Color("blue")
        # elif (audio_score >= 650 and audio_score < 850):
        #     leds.color = Color("purple")
        # elif (audio_score >= 850):
        #     leds.color = Color("white")

        # Read Stream Chunk
        chunk = stream.read(CHUNK_SIZE)

        # Calculate Audio Volume
        rms = ap.rms(chunk, 2)

        # Maintain Frame Buffer
        if (len(frame_buffer) == frame_buffer_size):
            frame_buffer.pop(0)

        # Update Frame Buffer
        frame_buffer.append(rms)

        # Calculate Normalize Audio Volume
        rms = normalize(rms, min(frame_buffer), max(frame_buffer)) * MAX_VALUE

        print(rms)

        # Error Correct Audio Score
        if (audio_score < 0):
            # Reset Audio Score
            audio_score = 0

        # Check Process Lock
        open(LOCK_FILE, "r")

# End LED Functions------------------------------------------------------------------------------------------------------------------------------------------------------------------

if (__name__ == "__main__"):
    # Start LED Control Loop
    while (True):
        # Initialize LEDs
        stream, leds = init_leds()

        # Start LED Animation
        try:
            animate_leds(stream, leds)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

# End Audio Processing File----------------------------------------------------------------------------------------------------------------------------------------------------------
