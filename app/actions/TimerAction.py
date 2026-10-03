from dataclasses import dataclass
from datetime import datetime
from typing import override, Any

from app.actions.AbstractAction import AbstractAction

@dataclass
class TimerAction(AbstractAction):
    duration:int
    
    @property
    @override
    def action_type(self) -> str:
        return "timer"

    @override
    def param_dict(self) -> dict[str, object]:
        param_dict:dict[str, object] = super().param_dict()
        param_dict["duration"] = self.duration
        return param_dict