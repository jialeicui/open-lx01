import random
import wave

from audio.vad import SpeechDetector


def test_vad() -> None:
    file = "data/test.wav"

    # read wav file
    with wave.open(file, "rb") as f:
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        assert nchannels == 1
        assert sampwidth == 2
        assert framerate == 16000
        data = f.readframes(nframes)

    # process the audio stream bytes
    sample_rate = 16000
    speech_detector = SpeechDetector(
        sample_rate=sample_rate, no_speech_duration_duration_ms=2000
    )

    first_silent = False
    silent_count = 0
    has_speech_count = 0
    frame_bytes = random.randint(1000, 2000)
    for i in range(0, len(data), frame_bytes):
        silent_for_a_long_time = speech_detector.process(data[i : i + frame_bytes])
        if not silent_for_a_long_time:
            first_silent = True
            silent_count += 1
            if speech_detector.has_speech:
                has_speech_count += 1
            speech_detector.reset()
        else:
            if first_silent and has_speech_count == 0:
                has_speech_count = 1

    print(f"has_speech_count: {has_speech_count}, silent_count: {silent_count}")


if __name__ == "__main__":
    test_vad()
