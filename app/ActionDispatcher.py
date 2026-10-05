import json

from app.Voice import Voice
from app.actions.AbstractAction import AbstractAction
from app.actions.GreetingAction import GreetingAction
from app.actions.TimerAction import TimerAction
from app.functionalities.timer import timer
from app.Player import Player
from typing import cast, Any
from datetime import datetime
from threading import Event


class ActionDispatcher:
    def __init__(self, voice:Voice, stop_event:Event) -> None:
        self.voice: Voice = voice
        self.stop_event: Event = stop_event

    def handle_request(self,request:str) -> bool:
        validated_action: AbstractAction | None = self.validate_command(request)
        
        if validated_action is None:
            Player.unvalid_command()
            self.voice.say("Perdona, no te he entendido.")
            return False
        
        try:
            self.dispatch_action(validated_action)
            return True
        except Exception:
            Player.unvalid_command()
            self.voice.say("Ha ocurrido un error.")
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

            case "greeting":
                if len(request_json) != 2:
                    return None
                response: Any | None = request_json.get("response")
                if response is None or not isinstance(response,str) or response == "":
                    return None
                return GreetingAction(request_time=datetime.now(),voice=self.voice,response=response,stop_event=self.stop_event)
                

            case "timer":
                if len(request_json) != 2:
                    return None
                duration: Any | None = request_json.get("duration")
                if duration is None or not isinstance(duration,int) or isinstance(duration, bool) or duration <= 0:
                    return None
                return TimerAction(request_time=datetime.now(),voice=self.voice,duration=duration,stop_event=self.stop_event)

            case "shutdown":
                self.stop_event.set()

            case _:
                return None
    
    def dispatch_action(self, action:AbstractAction) -> None:
        action.run()
