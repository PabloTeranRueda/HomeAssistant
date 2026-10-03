import json

from app.Voice import Voice
from app.actions.AbstractAction import AbstractAction
from app.actions.TimerAction import TimerAction
from app.functionalities.timer import timer
from typing import cast, Any
from datetime import datetime


class ActionDispatcher:
    def __init__(self, voice:Voice) -> None:
        self.voice = voice

    def handle_request(self,request:str) -> bool:
        validated_action: AbstractAction | None = self.validate_command(request)
        if validated_action is not None:
            try:
                self.dispatch_action(validated_action)
                return True
            except Exception:
                return False
        else:
            self.voice.say("Sorry, I did not understand you.")
            return False

    def validate_command(self, json_request:str) -> AbstractAction|None:
        if not isinstance(json_request,str) or json_request.strip() == "":
            return None

        try:
            request_json:Any = json.loads(json_request)
            if not isinstance(request_json,dict):
                return None
        except json.JSONDecodeError:
            return None

        action: Any | None = request_json.get("action")

        if not isinstance(action,str) or action.strip() == "":
            return None

        match action:

            case "timer":
                if len(request_json) != 2:
                    return None
                duration: Any | None = request_json.get("duration")
                if duration is None or not isinstance(duration,int) or isinstance(duration, bool) or duration <= 0:
                    return None
                return TimerAction(request_time=datetime.now(),duration=duration)
            case _:
                return None
    
    def dispatch_action(self, action:AbstractAction) -> None:
        match action.action_type:
            case "timer":
                timer_action = cast(TimerAction,action)
                timer(timer_action.duration,self.voice)
