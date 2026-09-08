from piper.voice import SynthesisConfig
import re
from pyaudio import PyAudio
from vosk import KaldiRecognizer, Model
import os
import vosk
import pyaudio
import json
from piper import PiperVoice

import wave
from pathlib import Path

# Checked audio device index with following script:
# for i in range(py_audio_setup.get_device_count()):
#     print(py_audio_setup.get_device_info_by_index(i))
INPUT_DEVICE_INDEX = 1

RECORDER_MODEL_PATH = "resources/vosk-model-es-0.42"
VOICE_MODEL_PATH = "resources/dii_es-ES.onnx"
#VOICE_MODEL_PATH = "resources/es_ES-sharvard-medium.onnx"
#VOICE_MODEL_PATH = "resources/dii_es-CO.onnx"
#VOICE_MODEL_PATH = "resources/miro_es-ES.onnx"

def init_input_stream():
    """
    Initializes and returns a PyAudio input stream for recording.
    """
    stream = py_audio_setup.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100, # Matches Vosk's expected rate
                    input=True,
                    frames_per_buffer=8192, # Size of audio chunks
                    input_device_index=INPUT_DEVICE_INDEX)
    return stream



def listen(stream, recognizer) -> str:
    while True:
        # Read audio data from the stream. exception_on_overflow=False prevents crashes
        # if the buffer temporarily can't keep up, instead it drops frames.
        data = stream.read(8192, exception_on_overflow=False)

        # Feed the audio data to the Vosk recognizer
        if not recognizer.AcceptWaveform(data):
            continue
        # If a complete phrase is recognized
        result = json.loads(recognizer.Result())
        text = result.get("text", "").strip() # Extract the recognized text

        if text:
            return text

def clear_stream(stream):
    available = stream.get_read_available()

    if available > 0:
        stream.read(
            available,
            exception_on_overflow=False
        )

    print(f"Cleared {available} frames")

def say(text, voice):
    output_stream = None

    try:
        config = SynthesisConfig(
            speaker_id=1
        )

        print("Using speaker:", config.speaker_id)

        for chunk in voice.synthesize(text, config):

            if output_stream is None:
                output_stream = py_audio_setup.open(
                    format=py_audio_setup.get_format_from_width(
                        chunk.sample_width
                    ),
                    channels=chunk.sample_channels,
                    rate=chunk.sample_rate,
                    output=True
                )

            output_stream.write(chunk.audio_int16_bytes)

    finally:
        if output_stream:
            output_stream.stop_stream()
            output_stream.close()

def say_test(text, voice):
    wav_path = Path(__file__).resolve().parent / "test.wav"

    with wave.open(str(wav_path), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    print("Created:", wav_path)

######## Initialize programme
if not os.path.exists(RECORDER_MODEL_PATH):
    print(f"Error: Vosk model not found at {RECORDER_MODEL_PATH}")
    print("Please download a model from https://alphacephei.com/vosk/models and unzip it into this directory.")
    exit(1)

recorder_model: Model = vosk.Model(RECORDER_MODEL_PATH)
voice_model: PiperVoice = PiperVoice.load(VOICE_MODEL_PATH)

recognizer: KaldiRecognizer = vosk.KaldiRecognizer(recorder_model, 44100) # 44100 Hz is common for Vosk models

py_audio_setup: PyAudio = pyaudio.PyAudio()

######## Initialize Audio Stream
print("Initializing STT. Listening... (Press Ctrl+C to stop)")
input_stream = init_input_stream()
input_stream.start_stream()

######## Listen key word
try:
    assistant_on:bool = True 
    while assistant_on:
        text: str = listen(input_stream,recognizer)
        print(input_stream)
        clear_stream(input_stream)
        print(input_stream)
        match text:
            case start if re.match(
                r"^h?acer(\s+)?h?ol(a+)$", start) or re.match(
                    r"^h?ol(a+)(\s+(h+)?a+)?(\s+)?h?acer$", start):
                say("¿En qué puedo ayudarte?",voice_model)
                continue
            case stop if re.match(r"^h?acer(\s+)?para$", stop) or re.match(
                r"^para(\s+(h+)?a+)?(\s+)?h?acer$", stop):
                
                assistant_on = False
            case _:
                print(text)
                continue
        

except KeyboardInterrupt:
    print("\nStopping STT listener.")
finally:
    input_stream.stop_stream()
    input_stream.close()
    py_audio_setup.terminate()