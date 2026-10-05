from winsound import PlaySound, SND_FILENAME, SND_ASYNC

class Player:

    @staticmethod
    def listener_ready():
        PlaySound(
                sound=r"resources/sounds/listener_ready.wav",
                flags=SND_FILENAME | SND_ASYNC
            )

    @staticmethod
    def listener_off():
        PlaySound(
                sound=r"resources/sounds/listener_off.wav",
                flags=SND_FILENAME | SND_ASYNC
            )

    @staticmethod
    def llm_working():
        PlaySound(
                sound=r"resources/sounds/llm_working.wav",
                flags=SND_FILENAME | SND_ASYNC
            )
    
    @staticmethod
    def timer_finished():
        PlaySound(
                sound=r"resources/sounds/timer_finished.wav",
                flags=SND_FILENAME | SND_ASYNC
            )

    @staticmethod
    def unvalid_command():
        PlaySound(
                sound=r"resources/sounds/unvalid_command.wav",
                flags=SND_FILENAME | SND_ASYNC
            )

    @staticmethod
    def command_received():
        PlaySound(
                sound=r"resources/sounds/command_received.wav",
                flags=SND_FILENAME | SND_ASYNC
            )