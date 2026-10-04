from threading import Thread, Event

from app.ActionDispatcher import ActionDispatcher
from app.LLM import LLM
from app.Listener import Listener
from app.Voice import Voice
from app.Player import Player


class Orchestrator:
    def __init__(self) -> None:
        self.stop_event = Event()
        self.voice = Voice()
        self.llm = LLM()
        self.action_dispatcher = ActionDispatcher(self.voice, self.stop_event)
        self.listener = Listener(self.stop_event)
        self.action_threads: list[Thread] = []

    def _cleanup_action_threads(self) -> None:
        for thread in self.action_threads.copy():
            if not thread.is_alive():
                thread.join()
                self.action_threads.remove(thread)

    def set_listener_on(self) -> None:
        ######## Initialize Audio Stream
        print("Initializing STT. Listening... (Press Ctrl+C to stop)")
        self.listener.start()
        Player.listener_ready()

        ######## Listen key word
        try:
            while not self.stop_event.is_set():
                self._cleanup_action_threads()

                user_input: str = self.listener.listen()

                if self.stop_event.is_set():
                    break
                
                Player.command_received()
                request = self.llm.interpret(user_input)

                if request.content is None:
                    Player.unvalid_command()
                    return

                thread: Thread = Thread(
                                    target=self.action_dispatcher.handle_request,
                                    args=(request.content,)
                                )
                
                self.action_threads.append(thread)
                thread.start()

                self.listener.clear()

        except KeyboardInterrupt:
            print("\nStopping STT listener.")
        finally:
            self.listener.close()
            for thread in self.action_threads:
                thread.join()
            Player.listener_off()