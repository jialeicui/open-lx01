import datetime
import pyaudio
import numpy as np
from scipy.signal import resample

from audio.vad import SpeechDetector

sample_format = pyaudio.paInt16
channels = 1
fs = 44100
chunk = fs // 2  # 500ms
p = pyaudio.PyAudio()


def resample_to_16k(content: bytes) -> bytes:
    """
    resample audio to 16k
    :param content: audio bytes
    :return: resampled audio bytes
    """
    content = np.frombuffer(content, dtype=np.int16)
    new_len = int(len(content) * 16000 / fs)
    return resample(content, new_len).astype(np.int16).tobytes()


print("recording...")

stream = p.open(
    format=sample_format,
    channels=channels,
    rate=fs,
    frames_per_buffer=chunk,
    input=True,
)

print(f"time now is {datetime.datetime.now()}")
speech_detector = SpeechDetector(no_speech_duration_duration_ms=4000)
while True:
    data = stream.read(chunk)
    silent_for_a_long_time = speech_detector.process(resample_to_16k(data))
    if not silent_for_a_long_time:
        print("no speech for a long time, {}".format(datetime.datetime.now()))
        break
