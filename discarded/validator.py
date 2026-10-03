import json
from typing import Any
from datetime import datetime

from actions.TimerAction import TimerAction
from actions.AbstractAction import AbstractAction

def validate_command(json_request:str) -> AbstractAction|None:
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