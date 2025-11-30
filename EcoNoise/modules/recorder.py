import sounddevice as sd
import numpy as np
import datetime

def capture_audio(duration=3, sample_rate=16000):
    """
    Records audio into memory only (NOT saved to disk).
    Returns (numpy_array, sample_rate, timestamp).
    """
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    # Flatten array
    audio = audio.flatten()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return audio, sample_rate, timestamp
