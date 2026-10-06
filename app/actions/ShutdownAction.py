from dataclasses import dataclass
from typing import override
from app.actions.AbstractAction import AbstractAction

@dataclass
class ShutdownAction(AbstractAction):
    
    @property
    @override
    def action_type(self) -> str:
        return "shutdown"

    @override
    def param_dict(self) -> dict[str, object]:
        param_dict:dict[str, object] = super().param_dict()
        return param_dict

    @override
    def run(self) -> None:
        self.voice.say("¡Hasta pronto!")