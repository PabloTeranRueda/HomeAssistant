import time

from Voice import Voice

def timer(seconds:int,voice:Voice) -> None:
    for remaining in range(seconds, 0, -1):
        voice.say(str(remaining))
        time.sleep(1)