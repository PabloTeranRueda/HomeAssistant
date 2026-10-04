from dataclasses import dataclass
from typing import override
from app.actions.AbstractAction import AbstractAction

@dataclass
class GreetingAction(AbstractAction):
    response:str
    
    @property
    @override
    def action_type(self) -> str:
        return "greeting"

    @override
    def param_dict(self) -> dict[str, object]:
        param_dict:dict[str, object] = super().param_dict()
        param_dict["response"] = self.response
        return param_dict
    
    @override
    def run(self) -> None:
        if self.stop_event.is_set():
            return
        self.voice.say(self.response)