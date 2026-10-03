import time

from app.Voice import Voice

def timer(seconds:int,voice:Voice) -> None:
    if not isinstance(seconds,int) or seconds < 0:
        return 
    for remaining in range(seconds, 0, -1):
        voice.say(str(remaining))
        time.sleep(1)