from pyaudio import PyAudio
import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer


class Recorder:
    """Handles microphone input and speech-to-text."""

    SAMPLE_RATE = 44100
    CHUNK_SIZE = 8192

    def __init__(self, model_path: str, input_device_index: int | None = None):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at {model_path}"
            )

        self.audio = pyaudio.PyAudio()
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(
            self.model,
            self.SAMPLE_RATE
        )

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.SAMPLE_RATE,
            input=True,
            frames_per_buffer=self.CHUNK_SIZE,
            input_device_index=input_device_index,
        )

    def start(self):
        """Start the microphone stream."""
        self.stream.start_stream()

    def stop(self):
        """Stop the microphone stream."""
        self.stream.stop_stream()

    def listen(self) -> str:
        """Listen for and return the next recognized phrase."""

        while True:
            data = self.stream.read(
                self.CHUNK_SIZE,
                exception_on_overflow=False
            )

            if not self.recognizer.AcceptWaveform(data):
                continue

            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip()

            if not isinstance(text,str):
                return ""

            return text.lower()

    def clear(self):
        """Discard audio currently waiting in the input buffer."""

        available = self.stream.get_read_available()

        if available > 0:
            self.stream.read(
                available,
                exception_on_overflow=False
            )

        print(f"Cleared {available} frames")

    def close(self):
        """Release microphone resources."""

        if self.stream.is_active():
            self.stream.stop_stream()

        self.stream.close()
        self.audio.terminate()