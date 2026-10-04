from threading import Event
import time

from app.Voice import Voice
from app.Player import Player

def timer(seconds:int,voice:Voice, stop_event:Event) -> None:
    if not isinstance(seconds,int) or seconds <= 0:
        return 
    for remaining in range(seconds, 0, -1):
        voice.say(str(remaining))
        stop_event.wait(1)
    
    Player.timer_finished()