import re
from ovos_number_parser import numbers_to_digits

from Recorder import Recorder
from Voice import Voice

from timer import timer
from threading import Thread

# Checked audio device index with following script:
# for i in range(py_audio_setup.get_device_count()):
#     print(py_audio_setup.get_device_info_by_index(i))
INPUT_DEVICE_INDEX = 1
SPEAKER_ID = 1

RECORDER_MODEL_PATH = "resources/vosk-model-es-0.42"
VOICE_MODEL_PATH = "resources/dii_es-ES.onnx"
#VOICE_MODEL_PATH = "resources/es_ES-sharvard-medium.onnx"
#VOICE_MODEL_PATH = "resources/dii_es-CO.onnx"
#VOICE_MODEL_PATH = "resources/miro_es-ES.onnx"

recorder = Recorder(model_path=RECORDER_MODEL_PATH, input_device_index=INPUT_DEVICE_INDEX)

voice = Voice(model_path=VOICE_MODEL_PATH, speaker_id=SPEAKER_ID)

######## Initialize Audio Stream
print("Initializing STT. Listening... (Press Ctrl+C to stop)")
recorder.start()

######## Listen key word
try:
    assistant_on:bool = True 
    while assistant_on:
        wake_phrase_is_correct:bool = False

        wake_phrase: str = recorder.listen()
        recorder.clear()
        match wake_phrase:
            case start if re.match(
                r"^h?acer(\s+)?h?ol(a+)$", start) or re.match(
                    r"^h?ol(a+)(\s+(h+)?a+)?(\s+)?h?acer$", start):
                
                wake_phrase_is_correct = True
                voice.say(text="¿En qué puedo ayudarte?")
                recorder.clear()

            case stop if re.match(r"^h?acer(\s+)?para$", stop) or re.match(
                r"^para(\s+(h+)?a+)?(\s+)?h?acer$", stop):
                wake_phrase_is_correct = False
                assistant_on = False
            case _:
                print(wake_phrase)
                wake_phrase_is_correct = False
                continue
        
        if not wake_phrase_is_correct:
            continue

        order: str = recorder.listen()

        match order:
            case temporizador if re.match(r"^(crea|pon).+?(temporizador|cuenta atrás)", temporizador):
                normalized_order = numbers_to_digits(order, "es")

                hours_match = re.search(r"(\d+)\s+hora(s)?", normalized_order)
                minutes_match = re.search(r"(\d+)\s+minuto(s)?", normalized_order)
                seconds_match = re.search(r"(\d+)\s+segundo(s)?", normalized_order)

                hours = int(minutes_match.group(1)) if minutes_match else 0
                minutes = int(minutes_match.group(1)) if minutes_match else 0
                seconds = int(seconds_match.group(1)) if seconds_match else 0

                total_seconds = (hours * 3600) + (minutes * 60) + seconds

                Thread(target = timer, kwargs={"seconds":total_seconds,"voice":voice}).start()

                recorder.clear()


        

except KeyboardInterrupt:
    print("\nStopping STT listener.")
finally:
    recorder.close()