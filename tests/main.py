from app.Voice import Voice
from app.ActionDispatcher import ActionDispatcher


SPEAKER_ID = 1
VOICE_MODEL_PATH = "resources/dii_es-ES.onnx"
VOICE: Voice = Voice(model_path=VOICE_MODEL_PATH, speaker_id=SPEAKER_ID)

dispatcher = ActionDispatcher(voice=VOICE)

# valid timer request
json_command = '{"action": "timer", "duration": 1}'
assert dispatcher.handle_request(json_command) is True

# timer with 0
json_command = '{"action": "timer", "duration": 0}'
assert dispatcher.handle_request(json_command) is False

# timer with a negative duration
json_command = '{"action": "timer", "duration": -1}'
assert dispatcher.handle_request(json_command) is False

# timer with a boolean duration
json_command = '{"action": "timer", "duration": True}'
assert dispatcher.handle_request(json_command) is False

# timer with an extra field
json_command = '{"action": "timer", "duration": 0, "other":0}'
assert dispatcher.handle_request(json_command) is False
# malformed JSON
json_command = '{"action": "timer", "duration": 0'
assert dispatcher.handle_request(json_command) is False
# unknown action
json_command = '{"action": "other", "duration": 0}'
assert dispatcher.handle_request(json_command) is False
# missing action
json_command = '{"duration": 0}'
assert dispatcher.handle_request(json_command) is False

