import webrtcvad


class SpeechDetector:
    """
    detect speech in audio stream
    """

    def __init__(
        self,
        aggressiveness=3,
        sample_rate=16000,
        frame_duration_ms=30,
        no_speech_duration_duration_ms=3000,
    ):
        self._vad = webrtcvad.Vad(aggressiveness)
        self._sample_rate = sample_rate
        self._frame_duration_ms = frame_duration_ms
        self._no_speech_duration_duration_bytes = (
            sample_rate * (no_speech_duration_duration_ms // 1000) * 2
        )
        # the whole audio stream bytes send to this instance
        self._audio_buffer = b""
        self._current_vad_frame = b""
        self._frame_bytes = int(
            sample_rate * (frame_duration_ms / 1000.0) * 2
        )  # 2 means 16bit

        # record the last speech position in the audio buffer, and reset the audio buffer when no speech for a long time
        self._last_speech_position = 0
        self._has_speech = False

    def reset(self):
        """
        reset the audio buffer, this make the instance can be reused
        """
        self._audio_buffer = b""
        self._current_vad_frame = b""
        self._last_speech_position = 0
        self._has_speech = False

    @property
    def bytes_content(self):
        return self._audio_buffer

    @property
    def has_speech(self):
        return self._has_speech

    def process(self, stream_bytes: bytes) -> bool:
        """
        process the audio stream bytes
        :param stream_bytes: audio stream bytes
        :return: True if speech detected, False if no speech for a long time
        """
        self._current_vad_frame += stream_bytes
        offset = 0
        while offset + self._frame_bytes < len(self._current_vad_frame):
            frame = self._current_vad_frame[offset : offset + self._frame_bytes]
            self._audio_buffer += frame
            if self._vad.is_speech(frame, self._sample_rate):
                # TODO optimize this memory copy
                self._last_speech_position = len(self._audio_buffer)
                self._has_speech = True
            else:
                if (
                    len(self._audio_buffer) - self._last_speech_position
                    > self._no_speech_duration_duration_bytes
                ):
                    return False
            offset += self._frame_bytes
        self._current_vad_frame = self._current_vad_frame[offset:]
        return True
