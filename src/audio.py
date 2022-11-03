# Developed by Nalin Ahuja, nalinahuja

import numpy as np
import pyaudio as pa
import audioop as ap

from gpiozero import RGBLED
from colorzero import Color

# End Imports------------------------------------------------------------------------------------------------------------------------------------------------------------

# Audio Constants
SAMPLE_RATE = 44100
CHUNK_SIZE = 2048
MAX_VALUE = 1000

# Time Constants
BUFFER_TIME = 2.50

# Process Lock File
LOCK_FILE = "./.lock"

# End Embedded Constants-------------------------------------------------------------------------------------------------------------------------------------------------

def unorm(value, min_value, max_value):
    # Normalize Input Value Inside Unit Interval
    return ((value - min_value) / (max_value - min_value + 1))

# End Helper Functions---------------------------------------------------------------------------------------------------------------------------------------------------

def animate_led():
    # Initialize GPIO Pins For LED Control
    # led = RGBLED(17, 22, 27, active_high = False)

    stream = pa.PyAudio()
    # Open Audio Stream Using PyAudio Interface
    stream = stream.open(format = pa.paInt16, input = True, channels = 2, rate = SAMPLE_RATE, frames_per_buffer = CHUNK_SIZE)

    # Create Process Lock File
    open(LOCK_FILE, "w")

    # Initialize Audio Score Metric
    audio_score = 0

    # Initialize Audio Frame Buffer
    frame_buffer, max_frame_buffer_len = [], int((SAMPLE_RATE / CHUNK_SIZE) * BUFFER_TIME)

    # Process Audio Stream
    while (True):
        """
        # Set LED Color By Audio Score
        if (audio_score < 150):
            led.color = Color("red")
        elif (audio_score >= 150 and audio_score < 350):
            led.color = Color("green")
        elif (audio_score >= 350 and audio_score < 650):
            led.color = Color("blue")
        elif (audio_score >= 650 and audio_score < 850):
            led.color = Color("purple")
        elif (audio_score >= 850):
            led.color = Color("white")
        """

        # Read Chunk From Stream
        chunk = stream.read(CHUNK_SIZE)

        # Calculate Audio Volume
        rms = ap.rms(chunk, 2)

        # Verify Frame Buffer Length
        if (len(frame_buffer) == max_frame_buffer_len):
            # Maintain Frame Buffer
            frame_buffer.pop(0)

        # Update Frame Buffer
        frame_buffer.append(rms)

        # Verify Buffer Is Populated
        if (len(frame_buffer) == 0):
            # Skip Iteration
            continue

        # Normalize Audio Volume To Range
        rms = unorm(rms, min(frame_buffer), max(frame_buffer)) * MAX_VALUE

        print("\r" + "\033[2K" + str("-" * int(rms / 100)) + "+", end = "")

        # Error Correct Audio Score
        if (audio_score < 0):
            # Reset Audio Score
            audio_score = 0

        # Check Process Lock
        open(LOCK_FILE, "r")

# End LED Functions------------------------------------------------------------------------------------------------------------------------------------------------------

if (__name__ == "__main__"):
    # Start LED Control Loop
    while (True):
        # Start LED Animation Loop
        try:
            animate_led()
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)

# End Audio Agent--------------------------------------------------------------------------------------------------------------------------------------------------------
