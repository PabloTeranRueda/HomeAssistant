from datetime import datetime
from threading import Event
from typing import Any


from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.Voice import Voice

@dataclass
class AbstractAction(ABC):
    request_time:datetime
    voice: Voice
    stop_event:Event

    @property
    @abstractmethod
    def action_type(self) -> str:
        ...
    
    def _base_param_dict(self) -> dict[str,object]:
        return{
            "request_time": self.request_time,
            "action_type": self.action_type
        }

    @abstractmethod
    def param_dict(self) -> dict[str,object]:
        return self._base_param_dict()

    @abstractmethod
    def run(self) -> None:
        ...