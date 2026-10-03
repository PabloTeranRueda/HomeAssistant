from piper import PiperVoice
from piper.config import SynthesisConfig
import pyaudio

class Voice:
    """Handles text-to-speech using Piper."""

    def __init__(self, model_path: str, speaker_id: int = 1):
        self.voice = PiperVoice.load(model_path)
        self.speaker_id = speaker_id
        self.audio = pyaudio.PyAudio()

    def say(self, text: str):
        """Synthesize and play text."""
        output_stream = None

        try:
            config = SynthesisConfig(
                speaker_id=self.speaker_id
            )

            print("Using speaker:", config.speaker_id)

            for chunk in self.voice.synthesize(text, config):

                if output_stream is None:
                    output_stream = self.audio.open(
                        format=self.audio.get_format_from_width(
                            chunk.sample_width
                        ),
                        channels=chunk.sample_channels,
                        rate=chunk.sample_rate,
                        output=True,
                    )

                output_stream.write(chunk.audio_int16_bytes)

        finally:
            if output_stream:
                output_stream.stop_stream()
                output_stream.close()

    def close(self):
        """Release audio resources."""
        self.audio.terminate()