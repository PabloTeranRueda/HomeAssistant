class LLMResponse:
    def __init__(self, thinking:str|None, content:str|None) -> None:
        self.thinking: str|None = thinking
        self.content:str|None = content