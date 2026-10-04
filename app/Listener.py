import os
from collections import deque
from threading import Event

import numpy as np
import sounddevice
from faster_whisper import WhisperModel


class Listener:
    """Handles microphone input and speech-to-text."""

    SAMPLE_RATE = 16000
    CHANNELS = 1

    CHUNK_DURATION = 0.1
    SILENCE_DURATION = 0.8
    PRE_ROLL_DURATION = 0.3

    ENERGY_THRESHOLD = 0.005
    REQUIRED_SPEECH_CHUNKS = 2

    def __init__(
        self,
        stop_event: Event,
        model_path: str = r"resources\whisper\small",
        input_device_index: int | None = None,
    ) -> None:

        if not os.path.isdir(model_path):
            raise FileNotFoundError(
                f"Whisper model not found at {model_path}"
            )

        self.stop_event: Event = stop_event

        self.model = WhisperModel(
            model_path,
            device="cpu",
            compute_type="int8",
        )

        self.input_device_index = input_device_index
        self._stream: sounddevice.InputStream | None = None

    def start(self) -> None:
        """Start the microphone."""

        if self._stream is not None:
            return

        self._stream = sounddevice.InputStream(
            samplerate=self.SAMPLE_RATE,
            channels=self.CHANNELS,
            dtype="float32",
            device=self.input_device_index,
        )

        self._stream.start()

    def listen(self) -> str:
        """Listen for one phrase and return its transcription."""

        if self._stream is None:
            self.start()

        assert self._stream is not None

        chunk_size = int(
            self.CHUNK_DURATION * self.SAMPLE_RATE
        )

        pre_roll_chunks = max(
            1,
            int(
                self.PRE_ROLL_DURATION
                / self.CHUNK_DURATION
            ),
        )

        pre_buffer: deque[np.ndarray] = deque(
            maxlen=pre_roll_chunks
        )

        audio_chunks: list[np.ndarray] = []

        speech_chunks = 0
        silence_duration = 0.0

        # Wait for speech.
        while not self.stop_event.is_set():

            chunk, _ = self._stream.read(chunk_size)

            chunk = np.asarray(
                chunk,
                dtype=np.float32,
            ).flatten()

            energy = float(
                np.sqrt(np.mean(chunk ** 2))
            )

            if energy > self.ENERGY_THRESHOLD:
                speech_chunks += 1
            else:
                speech_chunks = 0

            pre_buffer.append(chunk)

            if speech_chunks >= self.REQUIRED_SPEECH_CHUNKS:

                audio_chunks.extend(pre_buffer)

                break

        # Shutdown was requested while waiting for speech.
        if self.stop_event.is_set():
            return ""

        # Record until silence.
        while (
            silence_duration < self.SILENCE_DURATION
            and not self.stop_event.is_set()
        ):

            chunk, _ = self._stream.read(chunk_size)

            chunk = np.asarray(
                chunk,
                dtype=np.float32,
            ).flatten()

            audio_chunks.append(chunk)

            energy = float(
                np.sqrt(np.mean(chunk ** 2))
            )

            if energy <= self.ENERGY_THRESHOLD:
                silence_duration += self.CHUNK_DURATION
            else:
                silence_duration = 0.0

        # Shutdown was requested while recording.
        if self.stop_event.is_set():
            return ""

        audio = np.concatenate(audio_chunks)

        segments, _ = self.model.transcribe(
            audio,
            language="es",
            beam_size=5,
            vad_filter=False,
            initial_prompt="Tera es el nombre del asistente.",
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

    def stop(self) -> None:
        """Stop the microphone."""

        if self._stream is None:
            return

        if self._stream.active:
            self._stream.stop()

    def clear(self) -> None:
        """Discard pending microphone audio."""

        if self._stream is None:
            return

        chunk_size = int(
            self.CHUNK_DURATION * self.SAMPLE_RATE
        )

        while self._stream.read_available > 0:
            self._stream.read(
                min(
                    self._stream.read_available,
                    chunk_size,
                )
            )

    def close(self) -> None:
        """Release microphone resources."""

        if self._stream is None:
            return

        if self._stream.active:
            self._stream.stop()

        self._stream.close()
        self._stream = None


if __name__ == "__main__":
    stop_event = Event()

    listener = Listener(
        stop_event=stop_event
    )

    listener.start()

    try:
        while not stop_event.is_set():
            text = listener.listen()

            if text:
                print(text)

    except KeyboardInterrupt:
        stop_event.set()

    finally:
        listener.close()